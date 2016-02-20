from .value import PropertyValue, TaskOutputValue


class WorkflowInstance(object):
    def __init__(self):
        self.name = ''
        self.tasks = []
        self.tasks_dict = {}
        self.dependencies = {}
        self.context = None

    def set_name(self, name):
        self.name = name

    def add_task(self, task):
        self.tasks.append(task)
        self.tasks_dict[task.name] = task

    def set_context(self, context):
        self.context = context

    def compute_dependencies(self):
        for task in self.tasks:
            for dep in task.task.dependencies:
                task.add_dependency(self.tasks_dict.get(dep))

    def prepare_dict(self, value):
        if 'src' in value:
            src = value.get('src')
            if src == 'properties':
                key = value.get('key')
                return PropertyValue(key)
            elif src == 'taskout':
                task, output = value.get('key').split('.')
                return TaskOutputValue(self.tasks_dict.get(task), output)
        else:
            result = {}
            for k, v in value.items():
                if isinstance(v, dict):
                    v = self.prepare_dict(v)
                result.update({k:v})
            return result

    def prepare_inputs(self):
        for task in self.tasks:
            for key, value in task.inputs.items():
                if isinstance(value, dict):
                    value = self.prepare_dict(value)
                task.set_input(key, value)

    def resolve(self):
        pass # self.resolve_inputs()

    def run(self, scheduler=None):
        task_queue = []
        ready_queue = []
        success_queue = []
        failure_queue = []
        skipped_queue = []
        for task in self.tasks:
            task_queue.append(task)

        while len(task_queue) > 0:
            for task in task_queue:
                if task.is_ready():
                    task_queue.remove(task)
                    ready_queue.append(task)

            # Execute the ready queue
            for task in ready_queue:
                task.resolve_inputs()
                task.run()

            for task in ready_queue:
                ready_queue.remove(task)
                if task.is_successful():
                    success_queue.append(task)
                elif task.is_failure():
                    failure_queue.append(task)

    def __str__(self):
        return 'WorkflowInstance<%s>' % self.name

    def __repr__(self):
        return 'WorkflowInstance<%s>' % self.name
