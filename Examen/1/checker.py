import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    if not path.startswith("/"):
        path="/"+path
    return f"https://{host}{path}"
    pass


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("//https")
    pass


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    response=requests.get(url)
    print(f"Status:{response.status_code}")
    print(f"Content-Type:{response.headers.get('Content-Type')}")
    pass


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        response=requests.get(url, timeout=5)
        content_type=response.headers.get("Content-Type"," ")
        server=response.headers.get("Server","unknown")
        return {
            "status":response.status_code,
            "content_type":content_type,
            "length":len(response.content),
            "server":server,
        }
    except requests.RequestException as e:
        return {"status":None,"error":str(e)}
    pass


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results=[]
    success_count=0
    fail_count=0
    for url in SITES:
        res=check_site(url)
        results.append((url,res))
    working_sites=[item for item in results if item[1].get("status")==200]
    fail_count=len(results)-len(working_sites)
    success_count=len(working_sites)
    working_sites.sort(key=lambda x: x[1].get("length",0),reverse=True)
    for url,res in working_sites:
        print(f"{url} -> {res['status']}, {res['length']} octeți")
    print(f"Reușite:{success_count} Eșuate:{fail_count}")
    pass


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        response=requests.get(url,timeout=5)
        resp_headers={k.lower():v for k,v in response.headers.items()}
        present=[]
        missing=[]
        for header in SECURITY_HEADERS:
            if header.lower() in resp_headers:
                present.append(header)
            else:
                missing.append(header)
        score=int((len(present)/len(SECURITY_HEADERS))*100)
        return {"present":present,"missing":missing,"score":score}
    except requests.RequestException as e:
        return {"status":None,"error":str(e)}
    pass


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    current_attempt=0
    last_status=None
    last_error=None
    while current_attempt < attempts:
        current_attempt += 1
        try:
            response=requests.get(url,timeout=5)
            last_status=response.status_code
            if last_status < 500:
                return {"status":last_status,"attempts":current_attempt}
        except requests.RequestException as e:
            last_status=None
            last_error=str(e)
    result={"status":last_status,"attempts":current_attempt}
    if last_status is None and last_error:
        result["error"]=last_error
    return result
    pass
