
class StyleService:

    @staticmethod
    def register_view(style):
        style.views += 1
        style.save()

    @staticmethod
    def download(style):
        style.downloads += 1
        style.save()