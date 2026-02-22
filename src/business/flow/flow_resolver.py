from collections.abc import Callable

from business.flow.flow import IFlowManager
from domain.enums import State


# todo: Rename to ProcessMapper
def resolve(state: State, flow_manager: IFlowManager) -> Callable:

    resolved = {
        State.START : flow_manager.start,   # todo : this will require that whenever a new lead is created, the state is set to START, to be added in lead.start() in the same structure of lead.complete()
        State.GET_LANG: flow_manager.get_lang,
        State.GET_SERVICE: flow_manager.get_service,
        State.GET_SERVICE_BV: flow_manager.get_service_bv,
        State.GET_CITY: flow_manager.get_city,
        State.GET_DIM: flow_manager.get_dim,
        State.GET_ACTIVITY: flow_manager.get_activity, # todo: complete and unexpected should check if a closing message was sent and the lead was maraked as complete
        State.COMPLETE: flow_manager.complete
    }

    fn =  resolved.get(state, flow_manager.unexpected)

    print(f"Resolved : {fn}")

    return fn
