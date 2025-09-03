

import dns.resolver
import dns.reversename

def print_header(title: str):
    print("=" * 80)
    print(title)
    print("=" * 80)

def show_answers(name: str, rtype: str, resolver=None):
    res = resolver or dns.resolver.Resolver()
    try:
        ans = res.resolve(name, rtype)
        print(f"[{rtype}] {name}")
        for rdata in ans:
            print("   ", rdata.to_text())
    except dns.resolver.NXDOMAIN:
        print(f"[{rtype}] {name} -> (no existe)")
    except dns.resolver.NoAnswer:
        print(f"[{rtype}] {name} -> (sin respuesta)")

# A1
print_header("A1: A de yachaytech.edu.ec")
show_answers("yachaytech.edu.ec", "A")

# A2
print_header("A2: PTR de 8.8.8.8")
rev = dns.reversename.from_address("8.8.8.8")
show_answers(str(rev), "PTR")

# A3
print_header("A3: A de hpc.cedia.edu.ec usando 1.1.1.1")
res_cf = dns.resolver.Resolver(configure=False)
res_cf.nameservers = ["1.1.1.1"]
show_answers("hpc.cedia.edu.ec", "A", resolver=res_cf)

# A4
print_header("A4: MX de yachaytech.edu.ec")
show_answers("yachaytech.edu.ec", "MX")

# A5
print_header("A5: NS de yachaytech.edu.ec")
show_answers("yachaytech.edu.ec", "NS")

# A6
print_header("A6: SOA de yachaytech.edu.ec")
show_answers("yachaytech.edu.ec", "SOA")

# A7
print_header("A7: CNAME de www.microsoft.com")
show_answers("www.microsoft.com", "CNAME")

# A8
print_header("A8: Debug de yachaytech.edu.ec")
try:
    ans = dns.resolver.Resolver().resolve("yachaytech.edu.ec", "A")
    print(ans.response.to_text())
except Exception as e:
    print(f"(error en debug: {e})")

# A9
print_header("A9: Dominio inexistente")
show_answers("nonexistdomain12345.com", "A")
