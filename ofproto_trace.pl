#!/usr/bin/perl

my $BRIDGE="br-int";
#Ping fe:16:3e:86:fc:28/10.0.0.10 -> fa:16:3e:cc:bd:da/10.0.0.9
#my $INPUT_FLOW='in_port=10,dl_src=fa:16:3e:86:fc:28,dl_dst=fa:16:3e:cc:bd:da,icmp,nw_src=10.0.0.10,nw_dst=10.0.0.9';
my $IN_PORT="4";
my $ETH_DST="fa:16:3e:6c:a1:ad";
my $IP_DST="10.100.100.8";
#my $ETH_DST="fa:16:3e:a6:5a:a5";
#my $IP_DST="10.0.0.1";
my $ETH_SRC="fa:16:3e:1d:ca:a1";
my $IP_SRC="10.0.0.3";
#my $ETH_SRC="fa:16:3e:45:11:9d";
#my $IP_SRC="10.0.0.7";
my $INPUT_FLOW="in_port=$IN_PORT,dl_src=$ETH_SRC,dl_dst=$ETH_DST,icmp,nw_src=$IP_SRC,nw_dst=$IP_DST";
my $CT_STATE="new|trk";

###############################################################################

sub RemoveItemsFromFlow {
    # TODO Assuming no commas in flow field values
    my ($FLOW, $FIELD_NAME) = @_;
    $FLOW =~ s/$FIELD_NAME=[^,]*,?//;
    $FLOW =~ s/,$//;
    return $FLOW
}

sub AddItemsToFlow {
    my ($FLOW, $FIELD) = @_;
    my $FIELD_NAME;
    if ($FIELD =~ /^([^=]+)(=.+)?$/) {
        $FIELD_NAME=$1;
    } else {
        die "AddItmesToFlow: Bad field format: $FIELD"
    }
    $FLOW=RemoveItemsFromFlow($FLOW, $FIELD_NAME);
    return "$FLOW,$FIELD"
}

# Action handlers

sub ofproto_trace_recirc {
    my ($FLOW, $ACTION, $RECIRC_ID) = @_;
    return AddItemsToFlow($FLOW, "recirc_id=$RECIRC_ID");
}

sub ofproto_trace_ct {
    my ($FLOW, $ACTION, $CT_PARAMS) = @_;
    if ($CT_PARAMS =~ /zone=([0-9a-fA-Fx]+)/) {
        $FLOW = AddItemsToFlow($FLOW, "ct_zone=$1");
    }
    return AddItemsToFlow($FLOW, "ct_state=$CT_STATE");
}

my %action_hadlers = (
    "recirc" => \&ofproto_trace_recirc,
    "ct" => \&ofproto_trace_ct,
);

sub ofproto_trace {
    my $BRIDGE = $_[0];
    my $FLOW = $_[1];
    my $recurse = 0;
    $cmd = "sudo ovs-appctl ofproto/trace $BRIDGE '$FLOW' -generate";
    print "Executing: $cmd\n";
    open OUTPUT,'-|',$cmd || die "Bah!";

    while (<OUTPUT>) {
        # e.g. Final flow: icmp,reg6=0xd,metadata=0x1,in_port=10,vlan_tci=0x0000,dl_src=fe:16:3e:86:fc:28,dl_dst=fa:16:3e:cc:bd:da,nw_src=10.0.0.10,nw_dst=10.0.0.9,nw_tos=0,nw_ecn=0,nw_ttl=0,icmp_type=0,icmp_code=0
        if ($_ =~ /^Final flow:\s+(.+)$/) {
            $FLOW=$1 if ($1 ne "unchanged");
        # e.g. Datapath actions: ct(zone=1),recirc(0x50)
        #} elsif ($_ =~ /^Datapath actions:\s+ct\(([a-z0-9A-Z,=]*)\),recirc\(([0-9xa-fA-F]*)\)$/) {
        } elsif ($_ =~ /^Datapath actions:\s+(.*)$/) {
            # Actions appear to be: "drop", <int>, or func(...)
            # If drop or <int>: we're done. Otherwise, parse func and send
            # ... to external handler, which updates the FLOW
            my $actions=$1;
            #return if (($actions eq "drop") or ($actions =~ /^[0-9]+/));
            return if ($actions eq "drop");
            if ($actions =~ /^[0-9]+/) {
                # TODO I was sure I saw this output, but now I can't find it
                # So this block may be redundant
                print "DEBUG: Datapath action is a number: $actions\n";
                return;
            }

            $recurse=1;
            while ($actions =~ s/([a-zA-Z0-9_]*)\((.*?)\)//) {
                my $action_name=$1;
                my $action_args=$2;
                my $handler = $action_hadlers{$action_name};
                die "Cannot find handler for action: $action_name"
                        if ($handler == undef);
                $FLOW=$handler->($FLOW, $action_name, $action_args);
            }
        }
    } continue {
        print;
    }

    return if ($recurse == 0);

    return ofproto_trace($BRIDGE, $FLOW);
}


ofproto_trace($BRIDGE, $INPUT_FLOW);
