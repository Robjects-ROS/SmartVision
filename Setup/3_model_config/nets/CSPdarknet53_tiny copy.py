from functools import wraps
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Conv2D, Add, ZeroPadding2D, UpSampling2D, Concatenate, MaxPooling2D, Lambda, Layer, LeakyReLU, BatchNormalization
from tensorflow.keras.regularizers import l2
from utils.utils import compose
import tensorflow as tf

def route_group(input_layer, groups, group_id):
    # Split the channels evenly, we take the second part
    convs = tf.split(input_layer, num_or_size_splits=groups, axis=-1)
    return convs[group_id]

#--------------------------------------------------#
#   Single convolution
#--------------------------------------------------#
@wraps(Conv2D)
def DarknetConv2D(*args, **kwargs):
    # Added a regularization term
    # Regularization coefficient 5e-4
    darknet_conv_kwargs = {'kernel_regularizer': l2(5e-4)}
    darknet_conv_kwargs['padding'] = 'valid' if kwargs.get('strides')==(2,2) else 'same'
    darknet_conv_kwargs.update(kwargs)
    return Conv2D(*args, **darknet_conv_kwargs)

#---------------------------------------------------#
#   Convolution block
#   DarknetConv2D + BatchNormalization + LeakyReLU
#---------------------------------------------------#
def DarknetConv2D_BN_Leaky(*args, **kwargs):
    no_bias_kwargs = {'use_bias': False}
    no_bias_kwargs.update(kwargs)
    return compose( 
        DarknetConv2D(*args, **no_bias_kwargs),
        BatchNormalization(),
        LeakyReLU(alpha=0.1))

#---------------------------------------------------#
#   CSPdarknet structure block
#   There is a large residual edge
#   This large residual edge bypasses many residual structures
#---------------------------------------------------#
def resblock_body(x, num_filters):
    # Feature integration
    x = DarknetConv2D_BN_Leaky(num_filters, (3,3))(x)
    # Residual edge route
    route = x
    # Channel split
    x = Lambda(route_group,arguments={'groups':2, 'group_id':1})(x) 
    x = DarknetConv2D_BN_Leaky(int(num_filters/2), (3,3))(x)

    # Small residual edge route1
    route_1 = x
    x = DarknetConv2D_BN_Leaky(int(num_filters/2), (3,3))(x)
    # Stack
    x = Concatenate()([x, route_1])

    x = DarknetConv2D_BN_Leaky(num_filters, (1,1))(x)
    # The third resblockbody will lead to an effective feature layer branch
    feat = x
    # Connect
    x = Concatenate()([route, x])
    x = MaxPooling2D(pool_size=[2,2],)(x)

    # Finally, integrate the channels
    return x, feat

#---------------------------------------------------#
#   Main part of darknet53
#---------------------------------------------------#
def darknet_body(x):
    # Compress length and width
    x = ZeroPadding2D(((1,0),(1,0)))(x)
    # 416,416,3 -> 208,208,32
    x = DarknetConv2D_BN_Leaky(32, (3,3), strides=(2,2))(x)

    # Compress length and width
    x = ZeroPadding2D(((1,0),(1,0)))(x)
    # 208,208,32 -> 104,104,64
    x = DarknetConv2D_BN_Leaky(64, (3,3), strides=(2,2))(x)
    # 104,104,64 -> 52,52,128
    x, _ = resblock_body(x,num_filters = 64)
    # 52,52,128 -> 26,26,256
    x, _ = resblock_body(x,num_filters = 128)
    # 26,26,256 -> 13,13,512
    # feat1 shape = 26,26,256
    x, feat1 = resblock_body(x,num_filters = 256)

    x = DarknetConv2D_BN_Leaky(512, (3,3))(x)

    feat2 = x
    return feat1, feat2
