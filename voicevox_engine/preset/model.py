"""
プリセット機能に関して API と ENGINE 内部実装が共有するモデル（データ構造）

モデルの注意点は `voicevox_engine/model.py` の module docstring を確認すること。
"""

from pydantic import BaseModel, Field
from pydantic.json_schema import SkipJsonSchema

from voicevox_engine.metas.Metas import StyleId


class Preset(BaseModel):
    """
    プリセット情報
    """

    id: int = Field(title="プリセットID")
    name: str = Field(title="プリセット名")
    speaker_uuid: str = Field(title="話者のUUID")
    style_id: StyleId = Field(title="スタイルID")
    speedScale: float = Field(title="全体の話速")
    pitchScale: float = Field(title="全体の音高")
    intonationScale: float = Field(title="全体の抑揚")
    volumeScale: float = Field(title="全体の音量")
    prePhonemeLength: float = Field(title="音声の前の無音時間")
    postPhonemeLength: float = Field(title="音声の後の無音時間")
    pauseLength: float | SkipJsonSchema[None] = Field(
        default=None, title="句読点などの無音時間"
    )
    pauseLengthScale: float = Field(title="句読点などの無音時間（倍率）")
