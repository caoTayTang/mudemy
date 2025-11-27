from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from ..models.models import Resource

class ResourceService:
    def __init__(self, db_session: sessionmaker):
        self.db_session = db_session

    def create(self, resource_id: str, file_name: str, file_link: str,
               external_link: Optional[str] = None) -> Resource:
        resource = Resource(
            ResourceID=resource_id,
            File_Name=file_name,
            File_link=file_link,
            External_link=external_link
        )
        db = self.db_session()
        db.add(resource)
        db.commit()
        db.refresh(resource)
        db.close()
        return resource

    def get_by_id(self, resource_id: str) -> Optional[Resource]:
        db = self.db_session()
        result = db.query(Resource).filter(Resource.ResourceID == resource_id).first()
        db.close()
        return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Resource]:
        db = self.db_session()
        result = db.query(Resource).offset(skip).limit(limit).all()
        db.close()
        return result

    def get_by_file_name(self, file_name: str) -> List[Resource]:
        db = self.db_session()
        result = db.query(Resource).filter(Resource.File_Name.like(f'%{file_name}%')).all()
        db.close()
        return result

    def update(self, resource_id: str, file_name: Optional[str] = None,
               file_link: Optional[str] = None, external_link: Optional[str] = None) -> Optional[Resource]:
        db = self.db_session()
        resource = db.query(Resource).filter(Resource.ResourceID == resource_id).first()
        if not resource:
            db.close()
            return None
        
        if file_name is not None:
            resource.File_Name = file_name
        if file_link is not None:
            resource.File_link = file_link
        if external_link is not None:
            resource.External_link = external_link
        
        db.commit()
        db.refresh(resource)
        db.close()
        return resource

    def delete(self, resource_id: str) -> bool:
        db = self.db_session()
        resource = db.query(Resource).filter(Resource.ResourceID == resource_id).first()
        if not resource:
            db.close()
            return False
        
        db.delete(resource)
        db.commit()
        db.close()
        return True

    def attach_to_lesson(self, resource_id: str, lesson_id: str) -> bool:
        """Attach a resource to a lesson"""
        db = self.db_session()
        try:
            db.execute(provide_resource_table.insert().values(
                ResourceID=resource_id,
                LessonID=lesson_id
            ))
            db.commit()
            db.close()
            return True
        except:
            db.close()
            return False

    def detach_from_lesson(self, resource_id: str, lesson_id: str) -> bool:
        """Detach a resource from a lesson"""
        db = self.db_session()
        result = db.execute(
            provide_resource_table.delete().where(
                (provide_resource_table.c.ResourceID == resource_id) & 
                (provide_resource_table.c.LessonID == lesson_id)
            )
        )
        db.commit()
        db.close()
        return result.rowcount > 0

    def get_resources_by_lesson(self, lesson_id: str) -> List[Resource]:
        """Get all resources for a specific lesson"""
        db = self.db_session()
        result = db.execute(
            provide_resource_table.select().where(
                provide_resource_table.c.LessonID == lesson_id
            )
        ).fetchall()
        
        resource_ids = [row.ResourceID for row in result]
        resources = db.query(Resource).filter(Resource.ResourceID.in_(resource_ids)).all()
        db.close()
        return resources

    def get_lessons_by_resource(self, resource_id: str) -> List[str]:
        """Get all lesson IDs that use a specific resource"""
        db = self.db_session()
        result = db.execute(
            provide_resource_table.select().where(
                provide_resource_table.c.ResourceID == resource_id
            )
        ).fetchall()
        db.close()
        return [row.LessonID for row in result]

    def get_resource_usage_count(self, resource_id: str) -> int:
        """Get the number of lessons using this resource"""
        db = self.db_session()
        count = db.execute(
            provide_resource_table.select().where(
                provide_resource_table.c.ResourceID == resource_id
            )
        ).fetchall()
        db.close()
        return len(count)

    def detach_all_from_lesson(self, lesson_id: str) -> int:
        """Detach all resources from a specific lesson. Returns count of detached resources."""
        db = self.db_session()
        result = db.execute(
            provide_resource_table.delete().where(
                provide_resource_table.c.LessonID == lesson_id
            )
        )
        db.commit()
        count = result.rowcount
        db.close()
        return count

    def detach_all_from_resource(self, resource_id: str) -> int:
        """Detach a resource from all lessons. Returns count of affected lessons."""
        db = self.db_session()
        result = db.execute(
            provide_resource_table.delete().where(
                provide_resource_table.c.ResourceID == resource_id
            )
        )
        db.commit()
        count = result.rowcount
        db.close()
        return count

    def bulk_attach_to_lesson(self, lesson_id: str, resource_ids: List[str]) -> dict:
        """Attach multiple resources to a lesson at once"""
        db = self.db_session()
        success_count = 0
        failed_ids = []
        
        for resource_id in resource_ids:
            try:
                db.execute(provide_resource_table.insert().values(
                    ResourceID=resource_id,
                    LessonID=lesson_id
                ))
                success_count += 1
            except:
                failed_ids.append(resource_id)
        
        db.commit()
        db.close()
        
        return {
            'success': success_count,
            'failed': len(failed_ids),
            'failed_ids': failed_ids
        }

    def get_resource_stats(self, resource_id: str) -> dict:
        """Get statistics about a resource"""
        db = self.db_session()
        resource = db.query(Resource).filter(Resource.ResourceID == resource_id).first()
        
        if not resource:
            db.close()
            return {}
        
        lesson_count = db.execute(
            provide_resource_table.select().where(
                provide_resource_table.c.ResourceID == resource_id
            )
        ).fetchall()
        
        stats = {
            'resource_id': resource_id,
            'file_name': resource.File_Name,
            'file_link': resource.File_link,
            'external_link': resource.External_link,
            'used_in_lessons': len(lesson_count),
            'lesson_ids': [row.LessonID for row in lesson_count]
        }
        
        db.close()
        return stats