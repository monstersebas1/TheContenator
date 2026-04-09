"""TikTok video uploader."""


class TikTok:
    def __init__(self, account_id, nickname, firefox_profile):
        self.account_id = account_id
        self.nickname = nickname
        self.firefox_profile = firefox_profile

    def upload_video(self, video_path, title, description, hashtags):
        """Upload a video to TikTok."""
        raise NotImplementedError("TikTok upload not yet implemented")
