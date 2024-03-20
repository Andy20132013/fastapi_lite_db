from sqlalchemy import select
from database import TasksOrm, new_session
from schemas import STask, STaskAdd


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TasksOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls) -> list[STask]:
        async with new_session() as session:
            query = select(TasksOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            # print("****************")
            # for task_model in task_models:
            #     print("------------")
            #     print(task_model.__dict__)
            # print("++++++++++++++++++++")
            
            task_schemas = [STask.model_validate(
                task_model.__dict__) for task_model in task_models]
            return task_schemas
