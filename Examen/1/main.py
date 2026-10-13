from checker import (
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check,
)
print("PARTEA 1:Funcții")
print("fără /:",build_url("example.com","login"))
print("cu /:",build_url("example.com","/login"))
print("pe https:",is_https("https://example.com"))
print("pe http:",is_https("http://example.com"))
print("PARTEA 2:Trimiterea unei cereri")
print("Apel pentru https://example.com:")
show_response("https://example.com")
print("PARTEA 3:Un verificator reutilizabil")
print("pe site valid:",check_site("https://example.com"))
print("pe site invalid:",check_site("http://this-site-does-not-exist.invalid"))
print("PARTEA 4:Verificarea mai multor site-uri")
scan_sites()
print("PARTEA 5:Audit de securitate")
print("pe httpbin cu antete de securitate:",check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"))
print("pe example.com(fără antete de securitate specifice):",check_headers("https://example.com"))
print("PARTEA 6:Încercări repetate")
print("pe 200:",retry_check("https://httpbin.org/status/200"))
print("pe 404:",retry_check("https://httpbin.org/status/404"))
print("pe 500:",retry_check("https://httpbin.org/status/500"))