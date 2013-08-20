class DescartesError(Exception):
    pass


class SeriesError(DescartesError):
    pass


class ReportError(DescartesError):
    pass


class WebsiteError(DescartesError):
    pass
