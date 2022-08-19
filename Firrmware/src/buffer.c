#include <stdbool.h>
#include <stdint.h>
#include "buffer.h"

#define CBF_INC(v,mv)   ((((v) + 1) >= (mv)) ? 0 : (v) + 1)

uint8_t buffer_init(buffer_t *cb, uint8_t *area, uint16_t size)
{
	cb->buffer = area;
	cb->size = size;
	cb->prod = cb->cons = 0;

	return CBF_OK;
}

uint16_t buffer_bytes_available(buffer_t *cb)
{
    uint16_t flag_return = 0;

	if(cb->prod >= cb->cons)
		flag_return = cb->prod - cb->cons;
	else
		flag_return = cb->prod + (cb->size - cb->cons);

    return flag_return;    
}

uint8_t buffer_flush(buffer_t *cb)
{
	cb->prod = cb->cons = 0;

	return CBF_OK;
}

uint8_t buffer_get(buffer_t *cb, uint8_t *c)
{
    uint16_t flag_return = 0;

	if(cb->cons == cb->prod)
		flag_return = CBF_EMPTY;
    else
    {
        *c = cb->buffer[cb->cons];
	    cb->cons = CBF_INC(cb->cons,cb->size);

        flag_return = CBF_OK;
    }    	

	return flag_return;
}

uint8_t buffer_put(buffer_t *cb, uint8_t c)
{
	uint16_t next_prod = CBF_INC(cb->prod,cb->size);
    uint16_t flag_return = 0;

	if(next_prod == cb->cons)
		flag_return = CBF_FULL;
    else
    {
        cb->buffer[cb->prod] = c;
	    cb->prod = next_prod;

        flag_return = CBF_OK;
    }    	

	return flag_return;
}

