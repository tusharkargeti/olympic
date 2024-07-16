mkdir -p ~/.streamlit/

echo "\
[server]\n\
port= $PORT\n\
enableCOR = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml