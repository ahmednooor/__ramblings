package main

import (
	"fmt"
	events "./eventmanager"
)


// Event type will be modified by the one who emits the event
// and it should be visible to the listener, so the listener
// can convert the event arg passed as interface to this type
// to access members
type Event struct {
	eventVal	string
	// ... other event values
	
	eventTarget	*Widget // depends on the type that emits the event
}

// Widget is hypthetical here.
// it can be any other type like router, server etc.
type Widget struct {
	widgetVal	string
	// ... other widget values

	events.EventManager // this should come as it is to use events
}

func main() {
	w := Widget{
		"Some Widget Value",
		events.EventManager{},
	}

	w.AddEvent("isClicked", func(E interface{}) {
		e := E.(Event) // convert interfacce to Event type to access members
		fmt.Println("Widget Clicked")
		fmt.Println(e.eventVal)
		fmt.Println(e.eventTarget.widgetVal)
	})
	
	w.EmitEvent("isClicked", Event{"Some Event Value", &w})
	
	w.RemoveEvent("isClicked")	
}