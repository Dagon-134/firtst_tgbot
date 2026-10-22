from typing import LiteralString

from sql import Repo

class what_we_have:
    
    def get_tasks1(self, tg_id) -> LiteralString | None:
        repo = Repo()
        result = repo.watch(tg_id)
        if result is None:
            return
        formatted_tasks = [f"{item['task']} - {item['date_and_time']}" for item in result]
        final_change = []
        for i in formatted_tasks:
            i = i.replace(':00+03:00', '')
            final_change.append(i)
        fix_result = "\n".join(final_change)
        
        return fix_result
    
    def get_tasks2(self, list) -> LiteralString:
        formatted_tasks = [f"{item['time']} - {item['task']}" for item in list]
        final_change = []
        for i in formatted_tasks:
            i = i.replace(':00+03:00', '')
            final_change.append(i)
        fix_result = "\n".join(final_change)
        
        return fix_result