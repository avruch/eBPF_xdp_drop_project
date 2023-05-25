#include <uapi/linux/bpf.h>
#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h>
#include <linux/if_vlan.h>
#include <linux/ip.h>
#include <linux/ipv6.h>

//___________________________________BPF_Maps___________________________________//
BPF_ARRAY(user_param, int, 1); //storing user drop rate
BPF_ARRAY(random_param, int, 1); //storing the random pkt number
//______________________________________________________________________________//
int drop_func(struct xdp_md *ctx) {
    int rc = 0;
    uint32_t index=0;
    int *drop_val;
    int *param;
    drop_val=user_param.lookup(&index);  //pointer for the BPF map 
    param=random_param.lookup(&index);
    if(!drop_val){			  //BPF Security request
        return 0;
    }
    if(!param ){			  //BPF Security request
        return 0;
    }
    u32 randd= bpf_get_prandom_u32();	//randomizing with BPF function
    int randdd =randd % 100000; 	//100,000 for mili percent
    random_param.update(&index, &randdd);
    if(*param < *drop_val){		//
        rc= XDP_DROP;
        }
    else{
         rc=XDP_PASS;
    }
return rc;
}


