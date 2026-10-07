from sql import watch

class what_we_have:
    
    def get_tasks1(tg_id):
        result = watch(tg_id)
        formatted_tasks = [f"{item['task']} - {item['date_and_time']}" for item in result]
        final_change = []
        for i in formatted_tasks:
            i = i.replace(':00+03:00', '')
            final_change.append(i)
        fix_result = "\n".join(final_change)
        
        return fix_result
    
    def get_tasks2(list):
        formatted_tasks = [f"{item['time']} - {item['task']}" for item in list]
        final_change = []
        for i in formatted_tasks:
            i = i.replace(':00+03:00', '')
            final_change.append(i)
        fix_result = "\n".join(final_change)
        
        return fix_result