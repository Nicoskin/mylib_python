def corr(x, y, norm=True):
    """
    Вычисляет взаимную корреляцию двух одномерных массивов
    
    Параметры
    ------------
        x, y: одномерные массивы
        
        norm: есть нормирование или нет
        
        return:  корреляция
    """
    import numpy as np
    x = np.asarray(x)
    y = np.asarray(y)

    if norm:
        c = np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))
        return c
    else:
        c = np.dot(x, y)
        return c