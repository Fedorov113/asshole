class AnyFoundationClass(object):

    def __init__(self):
        # TODO add global debug here
        if 1 == 1:
            print('Created any foundation type class')


    def is_equal(self, other_any_ft_object):
        """
        Value equality.

        :param other_any_ft_object:
        :return:
        """
        if self == other_any_ft_object:
            return True
        else:
            return False

    # WTF
    def infix(self, other_any_ft_object):
        """
        Reference equality
        :param other_any_ft_object:
        :return:
        """
        return True

    def instance_of(self, a_type):
        """
        Create new instance of a type.

        :param a_type: type to create
        :return: AnyFT?
        """

        return True

    def type_of(self, other_any_ft_object):
        """
        Type name of an object as a string. May include generic parameters, as in "Interval<Time>".

        :param other_any_ft_object:
        :return:
        """
        a_type = ''
        return a_type