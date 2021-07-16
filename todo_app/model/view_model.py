class ViewModel:
    def __init__(self, items) -> None:
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        return list(filter(lambda i: i.status == 'To Do', self._items))

    @property
    def doing_items(self):
        return list(filter(lambda i: i.status == 'Doing', self._items))

    @property
    def done_items(self):
        return list(filter(lambda i: i.status == 'Done', self._items))
    
    @property
    def recent_done_items(self):
        return list(filter(lambda i: i.status == 'Done' and i.last_modified_today, self._items))

    @property
    def older_done_items(self):
        return list(filter(lambda i: i.status == 'Done' and not i.last_modified_today, self._items))

    @property
    def show_all_done_items(self):
        return len(self.done_items) < 5
