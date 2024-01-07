import unittest


class ExcludeDirTestLoader(unittest.TestLoader):
    def _match_path(self, path, full_path, pattern):
        # Exclude if the path contains directory name you want to exclude
        if "dump" in full_path:
            return False
        return super()._match_path(path, full_path, pattern)


if __name__ == "__main__":
    loader = ExcludeDirTestLoader()
    suite = loader.discover(".", pattern="test*.py")

    runner = unittest.TextTestRunner()
    runner.run(suite)
