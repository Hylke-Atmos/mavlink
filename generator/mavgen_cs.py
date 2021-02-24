#!/usr/bin/env python
'''
parse a MAVLink protocol XML file and generate a C# implementation

Copyright Michael Oborne 2018
Released under GNU GPL version 3 or later
'''

import sys, textwrap, os, time, re
from . import mavparse, mavtemplate

t = mavtemplate.MAVTemplate()

enumtypes = {}

map = {
        'float'    : 'float',
        'double'   : 'double',
        'char'     : 'byte',
        'int8_t'   : 'sbyte',
        'uint8_t'  : 'byte',
        'uint8_t_mavlink_version'  : 'B',
        'int16_t'  : 'short',
        'uint16_t' : 'ushort',
        'int32_t'  : 'int',
        'uint32_t' : 'uint',
        'int64_t'  : 'long',
        'uint64_t' : 'ulong',
    }
def cleanText(text):
    text = text.replace("\n"," ")
    text = text.replace("\r"," ")
    return text.replace("\"","'")
 
def normalize_enum_types(xml):
    print("normalize_enum_types: " + xml.filename)
    for m in xml.message:
        for fld in m.fields:
            if fld.enum != "" and fld.array_length == 0:
                enumtypes[fld.enum] = map[fld.type]

               
def generate_MAVLinkDeserializer(directory, xml_list):
    '''generate MAVLinkDeserializer in Utils directory'''
    utilsDir = os.path.join(directory, "Utils")

    print("Generating CSharp implementation in directory %s" % utilsDir)
    mavparse.mkdir_p(utilsDir)
    
    f = open(os.path.join(utilsDir, "MAVLinkDeserializer.cs"), mode='w')

    # sort msgs by id
    xml_msgs = []
    for xml in xml_list:
        for msg in xml.message:
            xml_msgs.append(msg)
    xml_msgs.sort(key=lambda msg: msg.id)

    f.write('''/// <Remark>
/// AUTO-GENERATED FILE.  DO NOT MODIFY.
/// 
/// This class was automatically generated by the
/// C# mavlink generator tool. It should not be modified by hand.
/// </Remark>
using System.Collections.Generic;

namespace MavLinkProtocol
{
    /// <summary>
    ///     Deserialization delegate to invoke the deserialization function of a specific message type.
    /// </summary>
    /// <typeparam name="T">MAVLink message type target template</typeparam>
    /// <param name="bytes">byte array in which the encoded MAVLink message is encapsulated.</param>
    /// <param name="isMavlink2">Flag to indicate if the MAVLink message is received as MAVLink V2 
    ///     message and therefor additional extra fields should expected</param>
    /// <returns>The decoded MAVLinkMessage</returns>
    internal delegate MAVLinkMessage MAVLinkMessageDeserializeFunc<T>(byte[] bytes, bool isMavlink2) where T : MAVLinkMessage;

    /// <summary>
    ///     MAVLink packet Info object containing the CRC_EXTRA value and a 
    ///     deserialization function to deserialize the MAVLink Message
    /// </summary>
    internal class MAVLinkDeserializer
    {
        /// <summary>
        ///     Deserialization delegate, to be used to deserialize a MAVLinkMessage.
        ///     Will return the decoded MAVLinkMessage.
        /// </summary>
        internal MAVLinkMessageDeserializeFunc<MAVLinkMessage> Unpack;
        /// <summary>
        ///     CRC extra byte used during parsing to validate of there is no incompatibility in dialect.
        /// </summary>
        internal byte CrcExtra;

        /// <summary>
        ///     Private constructor sinse these objects should only be created in the auto 
        ///     generated lookup table below.
        /// </summary>
        /// <param name="deserializeFunc">Instatiate function to deserialize the object should be 
        ///     references to <see cref="InstantiateType{T}(byte[], bool)"/>.</param>
        /// <param name="crcExtra">CRC extra byte</param>
        private MAVLinkDeserializer(MAVLinkMessageDeserializeFunc<MAVLinkMessage> deserializeFunc, byte crcExtra)
        {
            Unpack = deserializeFunc;
            CrcExtra = crcExtra;
        }

        /// <summary>
        ///     Method to instantiate a new object of MAVLinkMessage type <typeparamref name="T"/>
        /// </summary>
        /// <typeparam name="T">MAVLinkMessage type of which it should create and deserialze 
        ///     a new instance</typeparam>
        /// <param name="payload">encoded payload bytes</param>
        /// <param name="isMavlink2">Flag determining if it should be considered as MAVLinkV2</param>
        /// <returns>New MAVLinkMessage of the correct type</returns>
        private static MAVLinkMessage InstantiateType<T>(byte[] payload, bool isMavlink2) where T : MAVLinkMessage, new()
        {
            T obj = new T();
            obj.IsMavlink2 = isMavlink2;
            obj.Deserialize(payload);
            return obj;
        }

#pragma warning disable CS0618 // contains obsolete members but is auto generated, so can be ignored!
        internal static Dictionary<int, MAVLinkDeserializer> Lookup = new Dictionary<int, MAVLinkDeserializer>
        {
''')

    for msg in xml_msgs:
        t.write(f, '''            {Msg_${name_lower}.MSG_ID, new MAVLinkDeserializer(InstantiateType<Msg_${name_lower}>, Msg_${name_lower}.CRC_EXTRA)},
''', msg)
    f.write('''        };
    }
}''')
    f.close()

def generate_MAVLinkConstants(directory, xml_list):
    '''generate MAVLinkDeserializer in Utils directory'''
    utilsDir = os.path.join(directory, "Utils")

    print("Generating CSharp implementation in directory %s" % utilsDir)
    mavparse.mkdir_p(utilsDir)
    
    f = open(os.path.join(utilsDir, "MAVLinkConstants.cs"), mode='w')
    
    if xml_list[0].little_endian:
        xml_list[0].mavlink_little_endian = "true"
    else:
        xml_list[0].mavlink_little_endian = "false"
        
    t.write(f, '''/// <Remark>
/// AUTO-GENERATED FILE.  DO NOT MODIFY.
/// 
/// This class was automatically generated by the
/// C# mavlink generator tool. It should not be modified by hand.
/// </Remark>
namespace MavLinkProtocol
{

    public static class MAVLinkConstants
    {
        public const string MAVLINK_BUILD_DATE = "${parse_time}";
        public const string MAVLINK_WIRE_PROTOCOL_VERSION = "${wire_protocol_version}";
        public const byte MAVLINK_PROTOCOL_VERSION = ${version};

        internal const bool MAVLINK_LITTLE_ENDIAN = ${mavlink_little_endian};
    }
}''', xml_list[0])
    f.close()


def generate_message_enums(basename, xml): 
    print("generate_message_enums: " + xml.filename)
    # add some extra field attributes for convenience with arrays
    directory = os.path.join(basename, '''enums''')
    mavparse.mkdir_p(directory)
    
    normalize_enum_types(xml)
    
    for en in xml.enum:
        f = open(os.path.join(directory, en.name+".cs"), mode='w')
        
        en.description = cleanText(en.description)
        en.flags = ""
        if en.description.lower().find("bitmask") >= 0 or en.name.lower().find("_flags") >= 0:
            en.flags = '''
    [Flags]'''
        en.obsolete  = ""
        if en.deprecated:
            en.obsolete  = '''
    [Obsolete("%s | Replaced by: %s | since: %s")]''' % (cleanText(en.deprecated.description), en.deprecated.replaced_by, en.deprecated.since)
        en.enumtype = enumtypes.get(en.name,"int /*default*/")
        for fe in en.entry:
            if fe.name.endswith('ENUM_END'):
                en.entry.remove(fe)
                continue
            fe.description = cleanText(fe.description)
            fe.obsolete  = ""
            if fe.deprecated:
                fe.obsolete  = '''
        [Obsolete("%s | Replaced by: %s | since: %s")]''' % (cleanText(fe.deprecated.description), fe.deprecated.replaced_by, fe.deprecated.since)

        t.write(f, '''/// <Remark>
/// AUTO-GENERATED FILE.  DO NOT MODIFY.
/// 
/// This class was automatically generated by the
/// C# mavlink generator tool. It should not be modified by hand.
/// </Remark>
using System;
using static MavLinkProtocol.MAVLinkMessage;

namespace MavLinkProtocol
{
    /// <summary> 
    ///    ${description}
    /// </summary>${obsolete}${flags}
    public enum ${name} : ${enumtype}
    {
        ${{entry:
        /// <summary>
        ///    ${description} |${{param:${description}| }}
        /// </summary>${obsolete}
        [Description("${description}")]
        ${name}=${value},}}
    }
}''', en)
        f.close()

def generate_message_h(directory, m):
    '''generate per-message class file for a XML file'''
    f = open(os.path.join(directory, 'Msg_%s.cs' % m.name_lower), mode='w')
    
    m.obsolete = ""
    if m.deprecated:
        m.obsolete  = '''
    [Obsolete("%s | Replaced by: %s | since: %s")]''' % (cleanText(m.deprecated.description), m.deprecated.replaced_by, m.deprecated.since)
    
    t.write(f, '''/// <Remark>
/// AUTO-GENERATED FILE.  DO NOT MODIFY.
/// 
/// This class was automatically generated by the
/// C# mavlink generator tool. It should not be modified by hand.
/// </Remark>
using System;

namespace MavLinkProtocol
{
    /// <summary> 
    ///    ${description} 
    /// </summary>${obsolete}
    public class Msg_${name_lower} : MAVLinkMessage
    {
        public const int MSG_ID = ${id};
        internal const byte MAVLINK_MSG_MIN_LENGTH = ${wire_min_length};
        internal const byte MAVLINK_MSG_LENGTH = ${wire_length};
        internal const byte CRC_EXTRA = ${crc_extra};
        
        public sealed override int MsgId => MSG_ID;
        public sealed override int MsgLength => IsMavlink2 ? MAVLINK_MSG_LENGTH : MAVLINK_MSG_MIN_LENGTH;
        
        public sealed override string Name => "MAVLINK_MSG_ID_${name}";
        ${{ordered_fields:
        /// <summary>
        ///    ${description} ${enum} ${units} ${display}
        /// </summary>${unitsAttibute}
        [Description("${description}")]
        ${array_prefix} ${type} ${name};}}
        
        /// <summary>
        ///     Method to encode the <c><see cref="Msg_${name_lower}"/></c> object to a byte array.
        /// </summary>
        /// <remarks>
        ///     NOTE: This method does not include truncation of the byte array!
        /// </remarks>
        /// <returns>
        ///    (new) byte array of <see cref="MsgLength"/> containing the encoded form 
        ///    of this <c><see cref="Msg_${name_lower}"/></c> object.
        /// </returns>
        internal override byte[] Serialize()
        {
            byte[] payloadData = new byte[MAVLINK_MSG_LENGTH];
            ${{base_fields:${serialize_tag}
            }}
            if (IsMavlink2)
            {
                ${{extended_fields: ${serialize_tag}
                }}
            }
            return payloadData;
        }
        
        /// <summary>
        ///     Method to decode a byte array to this <c><see cref="Msg_${name_lower}"/></c> object.
        /// </summary>
        /// <remarks>
        ///     If the provided data array is not considered large enough (truncated),
        ///     it will be automatically appended with 0 value bytes at the end!
        /// </remarks>
        /// <param name="data">byte array containing the encoded form 
        ///    of this <c><see cref="Msg_${name_lower}"/></c> object.</param>
        internal override void Deserialize(byte[] payloadData)
        {
            ${{base_fields:${deserialize_tag}
            }}
            if (IsMavlink2)
            {
                ${{extended_fields: ${deserialize_tag}
                }}
            }
        }
        
        /// <summary>
        ///     Returns a string with the MSG name and data
        /// </summary>
        /// <returns>MSG name and data</returns>
        public override string ToString()
        {
            return Name + " -" + ${{ordered_fields:" ${name}:" + ${name} + }}"";
        }
    }
}''', m)
    f.close()

def generate_one(basename, xml):
    '''generate headers for one XML file'''
    
    directory = os.path.join(basename, xml.basename)

    print("Generating CSharp implementation in directory %s" % directory)
    mavparse.mkdir_p(directory)
    
    # add some extra field attributes for convenience with arrays
    for m in xml.message:
        m.msg_name = m.name
        if xml.crc_extra:
            m.crc_extra_arg = ", %s" % m.crc_extra
        else:
            m.crc_extra_arg = ""
        m.msg_nameid = "MAVLINK_MSG_ID_${name} = ${id}"
        m.description = cleanText(m.description)
        for f in m.fields:
            f.description = cleanText(f.description)
            if f.name == 'fixed':   # this is a keyword
                f.name = '@fixed'
            f.unitsAttibute = ''
            if f.units != "":
                f.unitsAttibute = '''
        [Units("%s")]''' % f.units
            f.decode_left = "%s.%s = " % (m.name_lower, f.name)
            f.decode_right = ''
            f.type = map[f.type] # use correct C# typing
            if f.array_length != 0:
                #f.array_prefix = '[MarshalAs(UnmanagedType.ByValArray,SizeConst=%u)]\n\t\tpublic' % f.array_length
                f.array_prefix = 'public'
                f.deserialize_tag = '%s = MAVLinkBitConverter.ConvertToType<%s>(payloadData, %d, %d);' % (f.name, f.type, f.wire_offset, f.array_length)
                f.serialize_tag = 'MAVLinkBitConverter.ToBytes(%s, payloadData, %d, %d);' % (f.name, f.wire_offset, f.array_length)
                f.type = "%s%s" % (f.type, '[]')
            else:
                f.array_prefix = 'public'
                f.deserialize_tag = '%s = MAVLinkBitConverter.ConvertToType<%s>(payloadData, %d);' % (f.name, f.type, f.wire_offset)
                f.serialize_tag = 'MAVLinkBitConverter.ToBytes(%s, payloadData, %d);' % (f.name, f.wire_offset)
                if f.enum != "":
                    f.deserialize_tag = '%s = (%s)MAVLinkBitConverter.ConvertToType<%s>(payloadData, %d);' % (f.name, f.enum, f.type, f.wire_offset)
                    f.serialize_tag = 'MAVLinkBitConverter.ToBytes((%s)%s, payloadData, %d);' % (f.type, f.name, f.wire_offset)
                    #f.type = "/*" +f.enum + "*/ " + f.type;
                    f.type = f.enum;

    # cope with uint8_t_mavlink_version
    for m in xml.message:
        m.arg_fields = []
        m.array_fields = []
        m.scalar_fields = []
        for f in m.ordered_fields:
            if f.array_length != 0:
                m.array_fields.append(f)
            else:
                m.scalar_fields.append(f)
        for f in m.fields:
            if not f.omit_arg:
                m.arg_fields.append(f)
                f.putname = f.name
            else:
                f.putname = f.const_value
                
    # separate base fields from MAVLink 2 extended fields
    for m in xml.message:
        m.base_fields = m.ordered_fields[:m.extensions_start]
        m.extended_fields = []
        if m.extensions_start is not None:
            m.extended_fields = m.ordered_fields[m.extensions_start:]
    
    for m in xml.message:
        generate_message_h(directory, m)

def copy_fixed_headers(directory, xml):
    '''copy the fixed protocol headers to the target directory'''
    import shutil, filecmp
    hlist = [ 'MAVLinkParser.cs', 'Utils/MAVLinkBitConverter.cs', 'Messages/MAVLinkAttributes.cs', 'Messages/MAVLinkCrc.cs', 'Messages/MAVLinkMessage.cs', 'Messages/MAVLinkPacket.cs', 'Messages/MAVLinkV2Packet.cs', 'MAVLinkProtocol.csproj' ]
        
    basepath = os.path.dirname(os.path.realpath(__file__))
    srcpath = os.path.join(basepath, 'CS')
    print("Copying fixed headers")
    for h in hlist:
        src = os.path.realpath(os.path.join(srcpath, h))
        dest = os.path.realpath(os.path.join(directory, h))
        if src == dest:
            continue
        destdir = os.path.realpath(os.path.join(directory, 'Messages'))
        if not os.path.exists(destdir): 
            os.makedirs(destdir)
        destdir = os.path.realpath(os.path.join(directory, 'Utils'))
        if not os.path.exists(destdir): 
            os.makedirs(destdir)
        shutil.copy(src, dest)


def generate(basename, xml_list):
    '''generate complete MAVLink CSharp implemenation'''
    print("generate for protocol %s to %s" % (xml_list[0].wire_protocol_version, basename))
    
    directory = basename

    if not os.path.exists(directory): 
        os.makedirs(directory) 

    for xml in xml_list:
        generate_message_enums(basename, xml)
        generate_one(basename, xml)
    
    generate_MAVLinkDeserializer(basename, xml_list)
    generate_MAVLinkConstants(basename, xml_list)
    copy_fixed_headers(basename, xml_list[0])
