from string import Template

NGINX_CONFIG_TEMPLATE: Template = Template(
    r"""server {
    server_name ${domain};
    location / {
        client_max_body_size 20000m;
        proxy_pass           http://127.0.0.1:${port};
    }
}
"""
)
