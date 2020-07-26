from ..abstract.node import Node
from typing import final
from ...io.virtual import create_virtual_connection
from .client import DeviceClient
from ....decorators import syft_decorator
from ....common.id import UID
from .device_type.device_type import DeviceType
from .device_type.unknown import unknown_device
from ..vm.vm import VirtualMachine
from ..vm.client import VirtualMachineClient
from typing import Dict
from ...message.syft_message import SyftMessage



@final
class Device(Node):

    client_type = DeviceClient

    child_type = VirtualMachine
    child_type_client_type = VirtualMachineClient

    @syft_decorator(typechecking=True)
    def __init__(
        self,
        name: str,
        device_type: DeviceType = unknown_device,
        vms: Dict[UID, VirtualMachine] = {},
    ):
        super().__init__(name=name)

        self.device_type = device_type

        self._register_services()

    def add_me_to_my_address(self):
        self.address.pri_address.device = self.id

    def message_is_for_me(self, msg: SyftMessage) -> bool:
        return (
            msg.address.pri_address.device == self.id
            and msg.address.pri_address.vm is None
        )