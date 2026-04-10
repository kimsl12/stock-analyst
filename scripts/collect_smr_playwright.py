#!/usr/bin/env python3
import os
import json
import time
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright
import requests
from bs4 import BeautifulSoup
try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None

SEEDS = [
    'https://www.nuscalepower.com/news',
    'https://www.rolls-royce.com/media/press-releases',
    'https://english.khnp.co.kr/',
    'https://www.kaeri.re.kr/english',
    'https://www.terrestrialenergy.com/news',
    'https://x-energy.com/news',
    'https://cfs.energy/news',
    'https://tae.com/news',
    'https://generalfusion.com/news',
    'https://www.helionenergy.com/news',
    'https://www.energy.gov/ne/nuclear-reactor-technologies/small-modular-reactors',
    'https://www.nrc.gov/reactors/advanced/small-modular-reactors.html',
    'https://www.onr.org.uk/smr/index.htm',
    'https://www.world-nuclear.org/information-library/nuclear-fuel-cycle/nuclear-power-reactors/small-nuclear-power-reactors.aspx',
    'https://www.iter.org/newsline',
]

OUTDIR = os.path.join(os.getcwd(), 'artifacts', 'smr_playwright_' + time.strftime('%Y%m%d_%H%M%S'))
os.makedirs(OUTDIR, exist_ok=True)

results = {
    'downloaded_files': [],
    'verified_records': [],
    'blocked_sources': [],
    'manual_downloads': [],
    'summary_notes': ''
}

def safe_filename(s):
    return s.replace('://', '_').replace('/', '_').replace('?', '_')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for url in SEEDS:
        try:
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0 Safari/537.36")
            page = context.new_page()
            print('Visiting', url)
            page.goto(url, wait_until='networkidle', timeout=60000)
            # Attempt to accept common cookie banners
            for sel in ["button:has-text(\"Accept\")", "button:has-text(\"I agree\")", "button:has-text(\"Agree\")", "button:has-text(\"Accept all\")", "button:has-text(\"동의\")", "button:has-text(\"확인\")"]:
                try:
                    locator = page.locator(sel)
                    if locator.count() > 0:
                        locator.first.click(timeout=3000)
                except Exception:
                    pass
            html = page.content()
            fname = os.path.join(OUTDIR, safe_filename(urlparse(url).netloc + urlparse(url).path) + '.html')
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(html)
            soup = BeautifulSoup(html, 'html.parser')
            pdfs = set()
            for a in soup.find_all('a', href=True):
                href = a['href']
                if '.pdf' in href.lower():
                    pdfs.add(urljoin(page.url, href))
            for link in soup.find_all('link', href=True):
                href = link['href']
                if '.pdf' in href.lower():
                    pdfs.add(urljoin(page.url, href))

            cookies = {c['name']: c.get('value', '') for c in context.cookies()}
            # Avoid using private Playwright internals (context._options) — use a stable UA string
            headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0 Safari/537.36"}

            # download PDFs via requests using cookies
            for pdf_url in pdfs:
                try:
                    r = requests.get(pdf_url, headers=headers, cookies=cookies, timeout=30, stream=True)
                    if r.status_code == 200:
                        local_pdf = os.path.join(OUTDIR, os.path.basename(urlparse(pdf_url).path))
                        with open(local_pdf, 'wb') as f:
                            for chunk in r.iter_content(1024*8):
                                f.write(chunk)
                        snippet = ''
                        if PdfReader is not None:
                            try:
                                reader = PdfReader(local_pdf)
                                text = ''
                                for p in reader.pages[:3]:
                                    text += (p.extract_text() or '')
                                snippet = text.strip()[:300]
                            except Exception:
                                snippet = ''
                        results['downloaded_files'].append({'local_path': local_pdf, 'url': pdf_url, 'file_type':'pdf', 'extracted_text_snippet': snippet})
                    else:
                        results['manual_downloads'].append({'url': pdf_url, 'reason': f'HTTP {r.status_code}', 'suggested_action': 'manual download or headless click'})
                except Exception as e:
                    results['blocked_sources'].append({'url': pdf_url, 'error': str(e)})

            results['downloaded_files'].append({'local_path': fname, 'url': url, 'file_type':'html', 'extracted_text_snippet': soup.get_text()[:300]})
            context.close()
        except Exception as e:
            results['blocked_sources'].append({'url': url, 'error': str(e)})
    browser.close()

results['summary_notes'] = f'Attempted {len(SEEDS)} seeds; downloaded {len(results["downloaded_files"])} artifacts; blocked {len(results["blocked_sources"])} sources.'
outpath = os.path.join(OUTDIR, 'smr_playwright_results.json')
with open(outpath, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print('Results saved to', outpath)
