from pydantic import BaseModel

class Project(BaseModel):
    pass

class ProjectCreate(Project):
    pass

class ProjectInDB(Project):
    pass

class ProjectReturn(ProjectInDB):
    name: str
    country = Column(String)
    city = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)

    # User relationship
    owner_id = Column(String, ForeignKey("users.id"))
    owner = relationship("User", back_populates="projects")

    # Records relationship
    records = relationship("Record", back_populates="project", cascade="all, delete")