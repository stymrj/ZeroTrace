"""Global configurations, constants, and target site registries."""

VERSION = "1.0.0"
DEFAULT_TIMEOUT = 7
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# Expandable list of target platforms for username reconnaissance.
# Designed for easy open-source contributions.
SOCIAL_TARGETS = [
    {"name": "GitHub", "url": "https://github.com/{}", "check": "status_200"},
    {"name": "Twitter / X", "url": "https://x.com/{}", "check": "status_200"},
    {"name": "Reddit", "url": "https://www.reddit.com/user/{}/about.json", "check": "json_data"},
    {"name": "Instagram", "url": "https://www.instagram.com/{}/", "check": "status_200"},
    {"name": "GitLab", "url": "https://gitlab.com/{}", "check": "status_200"},
    {"name": "Telegram", "url": "https://t.me/{}", "check": "status_200"},
    {"name": "Pinterest", "url": "https://www.pinterest.com/{}/", "check": "status_200"},
    {"name": "SoundCloud", "url": "https://soundcloud.com/{}", "check": "status_200"},
    {"name": "Medium", "url": "https://medium.com/@{}", "check": "status_200"},
    {"name": "Dev.to", "url": "https://dev.to/{}", "check": "status_200"},
    {"name": "HackerNews", "url": "https://news.ycombinator.com/user?id={}", "check": "status_200"},
    {"name": "Keybase", "url": "https://keybase.io/{}", "check": "status_200"},
    {"name": "Steam", "url": "https://steamcommunity.com/id/{}", "check": "status_200"},
    {"name": "Vimeo", "url": "https://vimeo.com/{}", "check": "status_200"},
    {"name": "Spotify", "url": "https://open.spotify.com/user/{}", "check": "status_200"},
    {"name": "Flickr", "url": "https://www.flickr.com/people/{}", "check": "status_200"},
    {"name": "Twitch", "url": "https://www.twitch.tv/{}", "check": "status_200"},
    {"name": "Dribbble", "url": "https://dribbble.com/{}", "check": "status_200"},
    {"name": "Behance", "url": "https://www.behance.net/{}", "check": "status_200"},
    {"name": "ProductHunt", "url": "https://www.producthunt.com/@{}", "check": "status_200"},
    {"name": "Disqus", "url": "https://disqus.com/by/{}/", "check": "status_200"},
    {"name": "About.me", "url": "https://about.me/{}", "check": "status_200"},
    {"name": "Patreon", "url": "https://www.patreon.com/{}", "check": "status_200"},
    {"name": "Bandcamp", "url": "https://{}.bandcamp.com", "check": "status_200"},
]
