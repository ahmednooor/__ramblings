package eventmanager


type EventManager struct {
	__events__	map[string]func(E interface{})
}

func (w *EventManager) AddEvent(eventName string, callback func(E interface{})) {
	if w.__events__ == nil {
		w.__events__ = make(map[string]func(E interface{}))
	}
	w.__events__[eventName] = callback
}

func (w *EventManager) EmitEvent(eventName string, E interface{}) {
	if _, ok := w.__events__[eventName]; ok && w.__events__ != nil {
		w.__events__[eventName](E)
	}
}

func (w *EventManager) RemoveEvent(eventName string) {
	if _, ok := w.__events__[eventName]; ok && w.__events__ != nil {
		delete(w.__events__, eventName)
	}
}
