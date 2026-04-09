"""Instagram Reels uploader."""


class Instagram:
    def __init__(self, account_id, nickname, firefox_profile):
        self.account_id = account_id
        self.nickname = nickname
        self.firefox_profile = firefox_profile

    def upload_reel(self, video_path, caption, hashtags):
        """Upload a reel to Instagram."""
        raise NotImplementedError("Instagram upload not yet implemented")
