package exercise

import "container/list"

type item struct{ key, value string }

type LRUCache struct {
	capacity int
	order    *list.List
	entries  map[string]*list.Element
}

func NewLRUCache(capacity int) *LRUCache {
	return &LRUCache{capacity, list.New(), make(map[string]*list.Element)}
}

func (c *LRUCache) Get(key string) (string, bool) {
	element, exists := c.entries[key]
	if !exists {
		return "", false
	}
	c.order.MoveToBack(element)
	return element.Value.(item).value, true
}

func (c *LRUCache) Put(key, value string) {
	if element, exists := c.entries[key]; exists {
		element.Value = item{key, value}
		c.order.MoveToBack(element)
		return
	}
	c.entries[key] = c.order.PushBack(item{key, value})
	if c.order.Len() > c.capacity {
		oldest := c.order.Front()
		delete(c.entries, oldest.Value.(item).key)
		c.order.Remove(oldest)
	}
}
