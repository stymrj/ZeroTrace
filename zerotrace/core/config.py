"""Global configurations, constants, and comprehensive target registries."""

VERSION = "1.1.0"
DEFAULT_TIMEOUT = 7
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)

SOCIAL_TARGETS = [
    {"name": "GitHub", "url": "https://github.com/{}", "check": "status_200", "cat": "Dev"},
    {"name": "GitLab", "url": "https://gitlab.com/{}", "check": "status_200", "cat": "Dev"},
    {"name": "Bitbucket", "url": "https://bitbucket.org/{}/", "check": "status_200", "cat": "Dev"},
    {"name": "Dev.to", "url": "https://dev.to/{}", "check": "status_200", "cat": "Dev"},
    {"name": "HackerNews", "url": "https://news.ycombinator.com/user?id={}", "check": "status_200", "cat": "Tech"},
    {"name": "Keybase", "url": "https://keybase.io/{}", "check": "status_200", "cat": "Security"},
    {"name": "DockerHub", "url": "https://hub.docker.com/u/{}/", "check": "status_200", "cat": "Dev"},
    {"name": "Kaggle", "url": "https://www.kaggle.com/{}", "check": "status_200", "cat": "Data/AI"},
    {"name": "Replit", "url": "https://replit.com/@{}", "check": "status_200", "cat": "Dev"},
    {"name": "Twitter / X", "url": "https://x.com/{}", "check": "status_200", "cat": "Social"},
    {"name": "Reddit", "url": "https://www.reddit.com/user/{}/about.json", "check": "json_data", "cat": "Social"},
    {"name": "Telegram", "url": "https://t.me/{}", "check": "status_200", "cat": "Social"},
    {"name": "Instagram", "url": "https://www.instagram.com/{}/", "check": "status_200", "cat": "Social"},
    {"name": "Pinterest", "url": "https://www.pinterest.com/{}/", "check": "status_200", "cat": "Social"},
    {"name": "Medium", "url": "https://medium.com/@{}", "check": "status_200", "cat": "Blogging"},
    {"name": "Steam", "url": "https://steamcommunity.com/id/{}", "check": "status_200", "cat": "Gaming"},
    {"name": "Twitch", "url": "https://www.twitch.tv/{}", "check": "status_200", "cat": "Streaming"},
    {"name": "Chess.com", "url": "https://www.chess.com/member/{}", "check": "status_200", "cat": "Gaming"},
    {"name": "SoundCloud", "url": "https://soundcloud.com/{}", "check": "status_200", "cat": "Music"},
    {"name": "Spotify", "url": "https://open.spotify.com/user/{}", "check": "status_200", "cat": "Music"},
    {"name": "ProductHunt", "url": "https://www.producthunt.com/@{}", "check": "status_200", "cat": "Community"},
    {"name": "About.me", "url": "https://about.me/{}", "check": "status_200", "cat": "Identity"}
]
