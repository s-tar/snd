class Storage:
    async def save(self, path, content):
        raise NotImplementedError

    def get_url(self, path):
        raise NotImplementedError
