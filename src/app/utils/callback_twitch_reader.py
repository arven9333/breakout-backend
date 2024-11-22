def get_html_for_reading_fragment(from_endpoint: str, to_endpoint: str):
    d = """
    <html>
       <head>
          <script>
             var url = window.location.href;
             const fragment = window.location.hash;
             const searchParams = new URLSearchParams(fragment.substring(1));
             url = url.replace('%s', '%s').replace(fragment, "");
             const newUrl = new URL(url);            
             for (const [key, value] of searchParams) {
                newUrl.searchParams.append(key, value);
            }
             window.location.replace(newUrl);
          </script>
       </head>
    </html>
    """ % (from_endpoint, to_endpoint)
    return d
