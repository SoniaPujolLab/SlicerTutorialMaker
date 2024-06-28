import requests
from dataclasses import dataclass

@dataclass
class GitFile:
    gitType: str
    path: str
    def __post_init__(self):
        self.files = {}
        self.url = ""
        pass
    def setFiles(self, files):
        self.files = files
        pass
    def dir(self, path="") -> list[str]:
        file = self.__file__(path)
        return list(file.files.keys())

    def getRaw(self, path:str) -> str:
        file = self.__file__(path)
        if file.gitType != "file":
            raise IOError(f"Expected file type, got {file.gitType} type")
        return requests.get(file.url).text

    def __file__(self, path:str):
        if path == "":
            return self
        spath = path.split("/")
        parent = self
        for seg in spath:
            if seg not in parent.files:
                raise IOError("Path does not exist")
            parent = parent.files[seg]
        return parent

class GitTools:

    def ParseRepo(repo:str, path="") -> GitFile:
        endpoint = f"https://api.github.com/repos/{repo}/contents{path}"
        contents = requests.get(endpoint).json()
        if not isinstance(contents, list) or not isinstance(contents[0], dict):
            if 'message' in contents:
                raise Exception(f"Message from {endpoint}: {contents['message']}")
            raise Exception(f"Malformed Response from {endpoint}")
        
        root = GitFile("dir", "")
        for data in contents:
            print(data)
            _file = GitFile(data["type"], data["path"])
            if _file.gitType == "dir":
                _file.setFiles(GitTools.__parseRecursive__(repo, data["path"]))
            elif _file.gitType == "file":
                _file.url = data["download_url"]
            root.files[data["name"]] = _file
        return root
    
    def __parseRecursive__(repo:str, path=""):
        endpoint = f"https://api.github.com/repos/{repo}/contents{path}"
        contents = requests.get(endpoint).json()
        if not isinstance(contents, list) or not isinstance(contents[0], dict):
            if contents.has_key('message'):
                raise Exception(f"Message from {endpoint}: {contents['message']}")
            raise Exception(f"Malformed Response from {endpoint}")
        
        files = {}
        for data in contents:
            _file = GitFile(data["type"], data["path"])
            if _file.gitType == "dir":
                _file.setFiles(GitTools.__parseRecursive__(repo, data["path"]))
            elif _file.gitType == "file":
                _file.url = data["download_url"]
            files[data["name"]] = _file
        return files
    
    def donwloadRepoZip(fullrepo:str, saveToPath:str, branch:str):
        fullurl = f"{fullrepo}/archive/refs/heads/{branch}"
        import SampleData
        dataLogic = SampleData.SampleDataLogic()
        downloadedFile = dataLogic.downloadFile(fullurl, saveToPath, branch)
        return downloadedFile
