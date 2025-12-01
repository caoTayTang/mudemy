from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Dict, Any
from ..models.models import Resource, ProvideResource


class ResourceService:
    """Service for Resource CRUD operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def create_resource(self, resource_data: Dict[str, Any]) -> Resource:
        """Create a new resource"""
        with self.db_session() as session:
            try:
                resource = Resource(**resource_data)
                session.add(resource)
                session.commit()
                session.refresh(resource)
                return resource
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error creating resource: {str(e)}")
    
    def get_resource_by_id(self, resource_id: str) -> Optional[Resource]:
        """Get resource by ID"""
        with self.db_session() as session:
            return session.query(Resource).filter(Resource.ResourceID == resource_id).first()
    
    def get_all_resources(self, skip: int = 0, limit: int = 100) -> List[Resource]:
        """Get all resources with pagination"""
        with self.db_session() as session:
            return session.query(Resource).offset(skip).limit(limit).all()
    
    def search_resources_by_name(self, name: str) -> List[Resource]:
        """Search resources by file name"""
        with self.db_session() as session:
            return session.query(Resource).filter(
                Resource.File_Name.like(f'%{name}%')
            ).all()
    
    def get_resources_with_external_links(self) -> List[Resource]:
        """Get all resources that have external links"""
        with self.db_session() as session:
            return session.query(Resource).filter(
                Resource.External_link.isnot(None)
            ).all()
    
    def update_resource(self, resource_id: str, update_data: Dict[str, Any]) -> Optional[Resource]:
        """Update resource information"""
        with self.db_session() as session:
            resource = session.query(Resource).filter(Resource.ResourceID == resource_id).first()
            if not resource:
                return None
            
            for key, value in update_data.items():
                if hasattr(resource, key):
                    setattr(resource, key, value)
            
            session.commit()
            session.refresh(resource)
            return resource
    
    def update_resource_file_link(self, resource_id: str, file_link: str) -> Optional[Resource]:
        """Update resource file link"""
        with self.db_session() as session:
            resource = session.query(Resource).filter(Resource.ResourceID == resource_id).first()
            if not resource:
                return None
            
            resource.File_link = file_link
            session.commit()
            session.refresh(resource)
            return resource
    
    def update_resource_external_link(self, resource_id: str, external_link: str) -> Optional[Resource]:
        """Update resource external link"""
        with self.db_session() as session:
            resource = session.query(Resource).filter(Resource.ResourceID == resource_id).first()
            if not resource:
                return None
            
            resource.External_link = external_link
            session.commit()
            session.refresh(resource)
            return resource
    
    def delete_resource(self, resource_id: str) -> bool:
        """Delete a resource"""
        with self.db_session() as session:
            resource = session.query(Resource).filter(Resource.ResourceID == resource_id).first()
            if not resource:
                return False
            
            session.delete(resource)
            session.commit()
            return True
    
    def get_resource_count(self) -> int:
        """Get total number of resources"""
        with self.db_session() as session:
            return session.query(Resource).count()


class ProvideResourceService:
    """Service for ProvideResource (Resource-Lesson relationship) operations"""
    
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session
    
    def provide_resource_to_lesson(self, resource_id: str, lesson_id: str) -> ProvideResource:
        """Assign a resource to a lesson"""
        with self.db_session() as session:
            try:
                provide = ProvideResource(ResourceID=resource_id, LessonID=lesson_id)
                session.add(provide)
                session.commit()
                session.refresh(provide)
                return provide
            except IntegrityError as e:
                session.rollback()
                raise ValueError(f"Error providing resource to lesson: {str(e)}")
    
    def get_provide_resource(self, resource_id: str, lesson_id: str) -> Optional[ProvideResource]:
        """Get a specific provide resource relationship"""
        with self.db_session() as session:
            return session.query(ProvideResource).filter(
                ProvideResource.ResourceID == resource_id,
                ProvideResource.LessonID == lesson_id
            ).first()
    
    def get_resources_by_lesson(self, lesson_id: str) -> List[ProvideResource]:
        """Get all resources provided for a specific lesson"""
        with self.db_session() as session:
            return session.query(ProvideResource).filter(
                ProvideResource.LessonID == lesson_id
            ).all()
    
    def get_lessons_by_resource(self, resource_id: str) -> List[ProvideResource]:
        """Get all lessons that use a specific resource"""
        with self.db_session() as session:
            return session.query(ProvideResource).filter(
                ProvideResource.ResourceID == resource_id
            ).all()
    
    def remove_resource_from_lesson(self, resource_id: str, lesson_id: str) -> bool:
        """Remove a resource from a lesson"""
        with self.db_session() as session:
            provide = session.query(ProvideResource).filter(
                ProvideResource.ResourceID == resource_id,
                ProvideResource.LessonID == lesson_id
            ).first()
            
            if not provide:
                return False
            
            session.delete(provide)
            session.commit()
            return True
    
    def remove_all_resources_from_lesson(self, lesson_id: str) -> bool:
        """Remove all resources from a lesson"""
        with self.db_session() as session:
            provides = session.query(ProvideResource).filter(
                ProvideResource.LessonID == lesson_id
            ).all()
            
            if not provides:
                return False
            
            for provide in provides:
                session.delete(provide)
            
            session.commit()
            return True
    
    def remove_resource_from_all_lessons(self, resource_id: str) -> bool:
        """Remove a resource from all lessons"""
        with self.db_session() as session:
            provides = session.query(ProvideResource).filter(
                ProvideResource.ResourceID == resource_id
            ).all()
            
            if not provides:
                return False
            
            for provide in provides:
                session.delete(provide)
            
            session.commit()
            return True
    
    def get_resource_count_by_lesson(self, lesson_id: str) -> int:
        """Get the number of resources for a lesson"""
        with self.db_session() as session:
            return session.query(ProvideResource).filter(
                ProvideResource.LessonID == lesson_id
            ).count()
    
    def get_lesson_count_by_resource(self, resource_id: str) -> int:
        """Get the number of lessons using a resource"""
        with self.db_session() as session:
            return session.query(ProvideResource).filter(
                ProvideResource.ResourceID == resource_id
            ).count()
    
    def is_resource_provided_to_lesson(self, resource_id: str, lesson_id: str) -> bool:
        """Check if a resource is provided to a lesson"""
        with self.db_session() as session:
            provide = session.query(ProvideResource).filter(
                ProvideResource.ResourceID == resource_id,
                ProvideResource.LessonID == lesson_id
            ).first()
            
            return provide is not None
    
    def bulk_provide_resources(self, resource_ids: List[str], lesson_id: str) -> List[ProvideResource]:
        """Provide multiple resources to a lesson"""
        with self.db_session() as session:
            provided = []
            
            for resource_id in resource_ids:
                try:
                    provide = ProvideResource(ResourceID=resource_id, LessonID=lesson_id)
                    session.add(provide)
                    provided.append(provide)
                except IntegrityError:
                    # Skip if already exists
                    continue
            
            session.commit()
            
            for provide in provided:
                session.refresh(provide)
            
            return provided
    
    def get_all_provide_resources(self) -> List[ProvideResource]:
        """Get all provide resource relationships"""
        with self.db_session() as session:
            return session.query(ProvideResource).all()