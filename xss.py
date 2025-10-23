#!/usr/bin/env python3
"""
XSS Scanner Professional Edition
Automated XSS Detection Tool with Professional Reporting
"""

import requests
import sys
import time
import random
import string
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

class XSSScanner:
    def __init__(self, target_url, delay=1, timeout=10):
        self.target_url = target_url
        self.delay = delay
        self.timeout = timeout
        self.session = requests.Session()
        self.found_vulnerabilities = []
        self.total_tests = 0
        self.successful_detections = 0
        self.failed_requests = 0
        
        # Set user agent
        user_agents = [
            "Mozilla/5.0 (Linux; Android 12; SM-S906N Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.94 Chrome/37.0.2062.94 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; SM-G996U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.023; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/94.0.4606.71 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 11; Pixel 5 Build/RQ3A.210805.001.A1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.159 Mobile Safari/537.36",
            "Mozilla/5.0 (X11; CrOS x86_64 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.7.12 (KHTML, like Gecko) Version/7.1.7 Safari/537.85.16",
            "Mozilla/5.0 (Windows NT 6.0; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Linux; Android 10; Google Pixel 4 Build/QD1A.190821.014.C2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Linux; Android 6.0.1; Nexus 6P Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 8_1_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B440 Safari/600.1.4",
            "Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; KFTT Build/IML74K) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 8_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12D508 Safari/600.1.4",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",
            "Mozilla/5.0 (Linux; Android 9; J8110 Build/55.0.A.0.552; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.99 Mobile Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53",
            "Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.6.3 (KHTML, like Gecko) Version/7.1.6 Safari/537.85.15",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.4.10 (KHTML, like Gecko) Version/8.0.4 Safari/600.4.10",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2",
            "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/12H321 Safari/600.1.4",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; rv:11.0) like Gecko",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B410 Safari/600.1.4",
            "Mozilla/5.0 (iPad; CPU OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11B554a Safari/9537.53",
            "Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Linux; Android 7.1.1; G8231 Build/41.2.A.0.219; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; TNJB; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; ARM; Trident/7.0; Touch; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MDDCJS; rv:11.0) like Gecko",
            "Mozilla/5.0 (Linux; Android 6.0.1; E6653 Build/32.2.A.0.253) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 10; HTC Desire 21 pro 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.127 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Linux; Android 6.0; HTC One X10 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.98 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H143 Safari/600.1.4",
            "Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFASWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) GSA/7.0.55539 Mobile/12H321 Safari/600.1.4",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; MATBJS; rv:11.0) like Gecko",
            "Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; KFJWI Build/IMM76D) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 7_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D167 Safari/9537.53",
            "Mozilla/5.0 (X11; CrOS armv7l 7077.134.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.156 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.2.5 (KHTML, like Gecko) Version/8.0.2 Safari/600.2.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11) AppleWebKit/601.1.56 (KHTML, like Gecko) Version/9.0 Safari/601.1.56",
            "Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFSOWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3",
            "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 8_1_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B435 Safari/600.1.4",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240",
            "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; MDDRJS; rv:11.0) like Gecko",
            "Mozilla/5.0 (Linux; U; Android 4.4.3; en-us; KFAPWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/3.68 like Chrome/39.0.2171.93 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; Touch; rv:11.0) like Gecko",
        ]
        self.session.headers.update({'User-Agent': random.choice(user_agents)})
    
    def print_banner(self):
        """Menampilkan banner profesional"""
        banner = """
        ██╗  ██╗███████╗███████╗   ████████╗██████╗ ██╗██╗  ██╗███████╗    
        ╚██╗██╔╝██╔════╝██╔════╝   ╚══██╔══╝██╔══██╗██║██║ ██╔╝██╔════╝    
         ╚███╔╝ ███████╗███████╗█████╗██║   ██████╔╝██║█████╔╝ █████╗      
         ██╔██╗ ╚════██║╚════██║╚════╝██║   ██╔══██╗██║██╔═██╗ ██╔══╝      
        ██╔╝ ██╗███████║███████║      ██║   ██║  ██║██║██║  ██╗███████╗    
        ╚═╝  ╚═╝╚══════╝╚══════╝      ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝

        [+] Author: Mr.ShadowX
        [+] GitHub: https://github.com/PhantomZero-X
        [+] Version: 1.0
        """
        print(banner)
    
    def show_success_message(self, vuln_type, location, payload_type, confidence):
        """Menampilkan pesan success yang profesional"""
        
        success_banner = """
\033[1;33m┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  \033[1;31m⚠️  \033[1;97mXSS VULNERABILITY DETECTED\033[1;33m                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\033[0m
        """
        print(success_banner)
        print(f"VULNERABILITY TYPE: {vuln_type}")
        print(f"LOCATION: {location}")
        print(f"PAYLOAD TYPE: {payload_type}")
        print(f"CONFIDENCE LEVEL: {confidence}")
        print(f"TIMESTAMP: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 70)
    
    def generate_payloads(self):
        """Generate XSS payloads dengan marker unik"""
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        marker = f"XSS{random_str}"
        
        payloads = [
            # Basic payloads
            {
                'payload': f"<script>alert('{marker}')</script>",
                'type': 'Script Tag Basic',
                'risk': 'HIGH'
            },
            {
                'payload': f"<img src=x onerror=alert('{marker}')>",
                'type': 'Image OnError',
                'risk': 'HIGH'
            },
            {
                'payload': f"<svg onload=alert('{marker}')>",
                'type': 'SVG OnLoad',
                'risk': 'HIGH'
            },
            {
                'payload': f"<body onload=alert('{marker}')>",
                'type': 'Body OnLoad',
                'risk': 'HIGH'
            },
            
            # Event handlers
            {
                'payload': f"<input onfocus=alert('{marker}') autofocus>",
                'type': 'Input OnFocus',
                'risk': 'MEDIUM'
            },
            {
                'payload': f"\" onmouseover=alert('{marker}') \"",
                'type': 'Double Quote Escape',
                'risk': 'MEDIUM'
            },
            {
                'payload': f"' onmouseover=alert('{marker}') '",
                'type': 'Single Quote Escape',
                'risk': 'MEDIUM'
            },
            
            # Advanced payloads
            {
                'payload': f"javascript:alert('{marker}')",
                'type': 'JavaScript URI',
                'risk': 'HIGH'
            },
            {
                'payload': f"<ScRiPt>alert('{marker}')</ScRiPt>",
                'type': 'Case Variation',
                'risk': 'MEDIUM'
            },
            {
                'payload': f"<img src=\"x\" `'` onclick=alert('{marker}')>",
                'type': 'Mixed Quotes',
                'risk': 'HIGH'
            },
        ]
        return payloads, marker
    
    def check_xss(self, response, payload_info, marker):
        """Check if XSS payload was successful dengan detail analysis"""
        try:
            payload = payload_info['payload']
            
            # Check 1: Basic reflection
            if marker in response.text:
                return True, "Payload Reflected", "MEDIUM"
            
            # Check 2: HTML context analysis
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check in script tags
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and marker in script.string:
                    return True, "Executable Context - Script Tag", "CRITICAL"
            
            # Check in event handlers
            for tag in soup.find_all(True):
                for attr, value in tag.attrs.items():
                    if isinstance(value, str) and marker in value and attr.startswith('on'):
                        return True, f"Executable Context - {attr} Handler", "CRITICAL"
            
            # Check in href attributes
            for tag in soup.find_all(href=True):
                if marker in tag['href'] and tag['href'].startswith('javascript:'):
                    return True, "Executable Context - JavaScript URI", "CRITICAL"
            
            # Check in attributes without events
            for tag in soup.find_all(True):
                for attr, value in tag.attrs.items():
                    if isinstance(value, str) and marker in value:
                        return True, f"Attribute Context - {attr}", "LOW"
            
            return False, "Not Reflected", "NONE"
            
        except Exception as e:
            return False, f"Error: {str(e)}", "NONE"
    
    def test_url_parameters(self, url):
        """Test URL parameters untuk XSS"""
        print(f"\n[PHASE 1] TESTING URL PARAMETERS: {url}")
        
        parsed_url = urlparse(url)
        if not parsed_url.query:
            print("   INFO: No URL parameters found")
            return
        
        from urllib.parse import parse_qs
        query_params = parse_qs(parsed_url.query)
        
        payloads, marker = self.generate_payloads()
        
        for param_name in query_params:
            print(f"   TESTING PARAMETER: {param_name}")
            
            for payload_info in payloads:
                self.total_tests += 1
                payload = payload_info['payload']
                
                try:
                    # Build test URL
                    test_params = query_params.copy()
                    test_params[param_name] = payload
                    
                    test_query = '&'.join([f"{k}={v[0]}" for k, v in test_params.items()])
                    test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{test_query}"
                    
                    # Send request
                    response = self.session.get(test_url, timeout=self.timeout)
                    
                    # Check for XSS
                    is_vulnerable, context, confidence = self.check_xss(response, payload_info, marker)
                    
                    if is_vulnerable:
                        self.successful_detections += 1
                        
                        vulnerability = {
                            'type': 'URL Parameter',
                            'location': param_name,
                            'payload': payload,
                            'payload_type': payload_info['type'],
                            'url': test_url,
                            'context': context,
                            'confidence': confidence,
                            'risk': payload_info['risk'],
                            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                        }
                        self.found_vulnerabilities.append(vulnerability)
                        
                        # Show SUCCESS message
                        self.show_success_message(
                            vuln_type="URL Parameter",
                            location=param_name,
                            payload_type=payload_info['type'],
                            confidence=confidence
                        )
                        
                        print(f"   CONTEXT: {context}")
                        print(f"   RISK LEVEL: {confidence}")
                        print(f"   PAYLOAD: {payload}")
                        print(f"   TEST URL: {test_url}")
                        print()
                        break
                    
                    time.sleep(self.delay)
                    
                except Exception as e:
                    print(f"   ERROR: {str(e)}")
                    self.failed_requests += 1
    
    def test_forms(self, url):
        """Test forms untuk XSS vulnerabilities"""
        print(f"\n[PHASE 2] TESTING FORMS: {url}")
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            forms = soup.find_all('form')
            
            if not forms:
                print("   INFO: No forms found")
                return
            
            print(f"   FOUND: {len(forms)} form(s)")
            
            for i, form in enumerate(forms, 1):
                print(f"   TESTING FORM: {i}")
                self.test_single_form(form, url)
                
        except Exception as e:
            print(f"   ERROR: {str(e)}")
            self.failed_requests += 1
    
    def test_single_form(self, form, base_url):
        """Test single form untuk XSS"""
        try:
            # Get form details
            action = form.get('action', '')
            method = form.get('method', 'get').lower()
            form_url = urljoin(base_url, action)
            
            # Find input fields
            inputs = form.find_all('input')
            textareas = form.find_all('textarea')
            all_fields = inputs + textareas
            
            input_fields = []
            for field in all_fields:
                field_name = field.get('name')
                if field_name and field.get('type') not in ['submit', 'button']:
                    input_fields.append(field_name)
            
            if not input_fields:
                print("      INFO: No input fields found")
                return
            
            print(f"      FIELDS: {', '.join(input_fields)}")
            
            payloads, marker = self.generate_payloads()
            
            # Test each field
            for field_name in input_fields:
                print(f"      TESTING FIELD: {field_name}")
                
                for payload_info in payloads:
                    self.total_tests += 1
                    payload = payload_info['payload']
                    
                    try:
                        # Prepare form data
                        form_data = {}
                        for field in input_fields:
                            if field == field_name:
                                form_data[field] = payload
                            else:
                                form_data[field] = "test"
                        
                        # Submit form
                        if method == 'post':
                            response = self.session.post(form_url, data=form_data, timeout=self.timeout)
                        else:
                            response = self.session.get(form_url, params=form_data, timeout=self.delay)
                        
                        # Check for XSS
                        is_vulnerable, context, confidence = self.check_xss(response, payload_info, marker)
                        
                        if is_vulnerable:
                            self.successful_detections += 1
                            
                            vulnerability = {
                                'type': 'Form Field',
                                'location': field_name,
                                'payload': payload,
                                'payload_type': payload_info['type'],
                                'url': form_url,
                                'method': method.upper(),
                                'context': context,
                                'confidence': confidence,
                                'risk': payload_info['risk'],
                                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                            }
                            self.found_vulnerabilities.append(vulnerability)
                            
                            # Show SUCCESS message
                            self.show_success_message(
                                vuln_type="Form Field",
                                location=field_name,
                                payload_type=payload_info['type'],
                                confidence=confidence
                            )
                            
                            print(f"      CONTEXT: {context}")
                            print(f"      RISK LEVEL: {confidence}")
                            print(f"      METHOD: {method.upper()}")
                            print(f"      PAYLOAD: {payload}")
                            print(f"      FORM URL: {form_url}")
                            print()
                            break
                        
                        time.sleep(self.delay)
                        
                    except Exception as e:
                        print(f"      ERROR: {str(e)}")
                        self.failed_requests += 1
                        
        except Exception as e:
            print(f"      FORM ERROR: {str(e)}")
            self.failed_requests += 1
    
    def start_scan(self):
        """Memulai scanning process"""
        print("\n[INITIATING SCAN] Starting comprehensive XSS security assessment...")
        print("=" * 70)
        
        start_time = time.time()
        
        try:
            # Test main URL parameters
            self.test_url_parameters(self.target_url)
            
            # Test forms on main page
            self.test_forms(self.target_url)
            
            # Find and test additional pages
            print("\n[PHASE 3] CRAWLING ADDITIONAL PAGES...")
            response = self.session.get(self.target_url, timeout=self.timeout)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            links = soup.find_all('a', href=True)
            found_urls = []
            
            for link in links:
                href = link['href']
                full_url = urljoin(self.target_url, href)
                
                # Only scan same domain
                if urlparse(full_url).netloc == urlparse(self.target_url).netloc:
                    if full_url not in found_urls and full_url != self.target_url:
                        found_urls.append(full_url)
            
            # Scan additional pages
            for url in found_urls[:3]:
                print(f"\n[ADDITIONAL PAGE] Testing: {url}")
                self.test_url_parameters(url)
                self.test_forms(url)
                time.sleep(self.delay)
                
        except Exception as e:
            print(f"SCAN ERROR: {str(e)}")
            self.failed_requests += 1
        
        end_time = time.time()
        self.scan_duration = end_time - start_time
    
    def generate_report(self):
        """Generate comprehensive professional scan report"""
        print("\n" + "=" * 80)
        print("SECURITY ASSESSMENT REPORT - XSS VULNERABILITY SCAN")
        print("=" * 80)
        
        # Calculate success rate
        success_rate = 100.0
        if self.total_tests > 0:
            success_rate = ((self.total_tests - self.failed_requests) / self.total_tests) * 100
        
        print(f"Scan Duration: {self.scan_duration:.2f} seconds")
        print(f"Total Tests Performed: {self.total_tests}")
        print(f"Vulnerabilities Identified: {self.successful_detections}")
        print(f"Failed Requests: {self.failed_requests}")
        print(f"Success Rate: {success_rate:.1f}%")
        print("-" * 80)
        
        if not self.found_vulnerabilities:
            print("ASSESSMENT RESULT: NO XSS VULNERABILITIES DETECTED")
            print("\nRECOMMENDATIONS:")
            print("  • Consider testing with additional payload variations")
            print("  • Test authenticated areas of the application")
            print("  • Perform manual testing for DOM-based XSS")
            print("  • Conduct security headers analysis")
            return
        
        print(f"ASSESSMENT RESULT: {len(self.found_vulnerabilities)} XSS VULNERABILITIES IDENTIFIED")
        
        # Group by confidence level
        critical_vulns = [v for v in self.found_vulnerabilities if v['confidence'] == 'CRITICAL']
        high_vulns = [v for v in self.found_vulnerabilities if v['confidence'] == 'HIGH']
        medium_vulns = [v for v in self.found_vulnerabilities if v['confidence'] == 'MEDIUM']
        low_vulns = [v for v in self.found_vulnerabilities if v['confidence'] == 'LOW']
        
        print(f"\nRISK ASSESSMENT SUMMARY:")
        print(f"  CRITICAL: {len(critical_vulns)}")
        print(f"  HIGH: {len(high_vulns)}")
        print(f"  MEDIUM: {len(medium_vulns)}")
        print(f"  LOW: {len(low_vulns)}")
        
        # Print detailed findings
        print(f"\nDETAILED VULNERABILITY FINDINGS:")
        print("-" * 80)
        
        for i, vuln in enumerate(self.found_vulnerabilities, 1):
            print(f"\n[{i}] {vuln['type'].upper()} - {vuln['confidence']} RISK")
            print(f"    Location: {vuln['location']}")
            print(f"    Context: {vuln['context']}")
            print(f"    Payload Type: {vuln['payload_type']}")
            if vuln['type'] == 'Form Field':
                print(f"    HTTP Method: {vuln['method']}")
            print(f"    Timestamp: {vuln['timestamp']}")
            print(f"    URL: {vuln['url']}")
            print(f"    Payload: {vuln['payload']}")

def main():
    """Main function"""
    # Initialize scanner
    scanner = XSSScanner("", delay=0.5, timeout=10)
    scanner.print_banner()
    
    # Get URL input
    while True:
        try:
            url = input("\nEnter target URL (include http/https): ").strip()
            
            if not url:
                print("ERROR: URL cannot be empty")
                continue
                
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
                
            # Validate URL
            parsed = urlparse(url)
            if not parsed.netloc:
                print("ERROR: Invalid URL format")
                continue
                
            scanner.target_url = url
            break
            
        except KeyboardInterrupt:
            print("\n\nScan cancelled by user")
            sys.exit(0)
        except Exception as e:
            print(f"ERROR: {str(e)}")
    
    # Start scanning
    try:
        scanner.start_scan()
        scanner.generate_report()
        
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user")
        scanner.generate_report()
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {str(e)}")

if __name__ == "__main__":
    main()