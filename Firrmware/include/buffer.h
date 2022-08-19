//#pragma once
#ifndef CBF_H

#define CBF_H

#define CBF_OK      0 
#define CBF_FULL    1  
#define CBF_EMPTY   2  

typedef struct buffer_s
{
	volatile uint16_t prod; 
	volatile uint16_t cons; 
	uint16_t size;          
    uint8_t *buffer;        
} buffer_t;

uint16_t buffer_bytes_available(buffer_t *cb);
uint8_t buffer_flush(buffer_t *cb);
uint8_t buffer_get(buffer_t *cb, uint8_t *c);
uint8_t buffer_init(buffer_t *cb, uint8_t *area, uint16_t size);
uint8_t buffer_put(buffer_t *cb, uint8_t c);


#endif