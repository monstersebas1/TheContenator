"""Facebook Reels/video uploader."""


class Facebook:
    def __init__(self, account_id, nickname, firefox_profile):
        self.account_id = account_id
        self.nickname = nickname
        self.firefox_profile = firefox_profile

    def upload_video(self, video_path, title, description):
        """Upload a video to Facebook."""
        raise NotImplementedError("Facebook upload not yet implemented")
