from sqlmodel import SQLModel, Field

class Song(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    artist: str
    album: str
    spotify_id: str
    cover_image_url: str  # Add this line
