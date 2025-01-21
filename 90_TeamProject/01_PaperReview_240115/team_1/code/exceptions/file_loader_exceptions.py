# exceptions/file_loader_exceptions.py

class FileLoaderError(Exception):
    """기본 파일 로더 예외 클래스"""
    pass

class InvalidFileExtensionError(FileLoaderError):
    """유효하지 않은 파일 확장자 예외"""
    pass

class DirectoryTraversalError(FileLoaderError):
    """디렉토리 트래버설 공격 방지 예외"""
    pass

class YamlParsingError(FileLoaderError):
    """YAML 파싱 중 발생한 예외"""
    pass

class PdfProcessingError(FileLoaderError):
    """PDF 처리 중 발생한 예외"""
    pass
