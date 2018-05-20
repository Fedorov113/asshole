class ObjectRef:

    def __init__(self, namespace, type, id):
        """

        :param namespace:
        :param type:
        :param id: it is ObjectID!
        """

        # TODO None checking
        self.namespace = namespace
        self.type = type
        self.id = id