from datetime import datetime

def validate_visit_data(data):
    errors = []
    
    if not data.get('doctor_id'):
        errors.append("Не выбран врач")
    
    if not data.get('service_id'):
        errors.append("Не выбрана услуга")
    
    try:
        datetime.strptime(data['date'], "%Y-%m-%d")
    except ValueError:
        errors.append("Неверный формат даты")
    
    return errors

def validate_service_data(data):
    errors = []
    if not data.get('name'):
        errors.append("Название услуги обязательно")
    if not data.get('base_cost') or data['base_cost'] <= 0:
        errors.append("Некорректная стоимость")
    return errors