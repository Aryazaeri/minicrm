import enum


class PipelineStage(str, enum.Enum):
    new = "new"
    contacted = "contacted"
    negotiating = "negotiating"
    won = "won"
    lost = "lost"
