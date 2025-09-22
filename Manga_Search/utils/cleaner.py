import re

def clean_story_data(story_data: dict) -> dict:
    if not story_data:
        return story_data

    # Làm sạch cốt truyện
    if "Cốt truyện" in story_data and isinstance(story_data["Cốt truyện"], str):
        ILLEGAL_CHARACTERS_RE = re.compile(r"[\000-\010]|[\013-\014]|[\016-\037]")
        story_data["Cốt truyện"] = ILLEGAL_CHARACTERS_RE.sub("", story_data["Cốt truyện"]).strip()

    # Chuẩn hóa tags
    if "Tags" in story_data and isinstance(story_data["Tags"], str):
        tags = [t.strip().lower() for t in story_data["Tags"].split(",") if t.strip()]
        story_data["Tags"] = ", ".join(sorted(set(tags)))

    # Chuẩn hóa trạng thái
    if "Trạng thái" in story_data:
        status = story_data["Trạng thái"].lower()
        if "hoàn" in status:
            story_data["Trạng thái"] = "Hoàn thành"
        elif "đang" in status:
            story_data["Trạng thái"] = "Đang ra"
        else:
            story_data["Trạng thái"] = "Khác"

    return story_data
