# Standard
import abc


class EmailInterface(metaclass=abc.ABCMeta):

    @abc.abstractclassmethod
    def send(cls, mail, trials=6):
        """Abstract Class Method that handles sending mail using SendGrid API

        Args:
            mail (instance): an instance of SendGrid's Mail class.
            trials (int): The maximum number the  email submit resent in case a GatewayTimeoutError is raised.
        """
        pass
