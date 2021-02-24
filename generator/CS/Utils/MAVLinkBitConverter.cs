﻿/// <Remark>
/// AUTO-GENERATED FILE.  DO NOT MODIFY.
/// 
/// This class was automatically generated by the
/// C# mavlink generator tool. It should not be modified by hand.
/// </Remark>
using System;
using System.Runtime.InteropServices;

namespace MavLinkProtocol
{
    /// <summary>
    ///     Helper class to convert any byte[] to => primitive types or type[]
    ///     and helps converting primitive types and type[] back to byte[].
    ///     Delegates the actual prasing to the .Net framework bitconverter for speed, 
    ///     but makes sure the byte alignment is correct (Little vs. Big endian).
    /// </summary>
    public static class MAVLinkBitConverter
    {
        public static readonly bool MAVLINK_NEED_BYTE_SWAP = MAVLinkConstants.MAVLINK_LITTLE_ENDIAN && !BitConverter.IsLittleEndian;

        #region Deserialization
        /// <summary>
        ///     Resizes a byte array if the byte array is not large enough to contain a value of 
        ///     (primitive) type <typeparamref name="T"/>.
        /// </summary>
        /// <typeparam name="T">(Primitive) type to check the array size against</typeparam>
        /// <param name="bytes">Reference to byte array containing a value of primative type <typeparamref name="T"/></param>
        /// <param name="startoffset">Stating position in the array of the value</param>
        private static void ResizeIfNeccesary<T>(ref byte[] bytes, int startoffset) where T : struct
        {
            int sizeOfType = Marshal.SizeOf(default(T));
            if (bytes.Length >= startoffset + sizeOfType) return;
            Array.Resize(ref bytes, startoffset + sizeOfType);
        }

        /// <summary>
        ///     Converts a byte array to a value of the expected (primative) type.
        ///     Only the amount of required bytes for the type are evaluated.
        ///     if the provided byte array is not large enough (not enough bytes) for the 
        ///     desired return type, additional bytes will be adde to the end of the byte array.
        /// </summary>
        /// <typeparam name="T">(Primitive) type of the expected return value</typeparam>
        /// <param name="value">Byte array containing a value that need to be converted to a primative type <typeparamref name="T"/></param>
        /// <param name="startIndex">Stating position in the array of the value</param>
        /// <returns>Value converted in (primitive) type <typeparamref name="T"/></returns>
        /// <exception cref="NotSupportedException">Thown if <typeparamref name="T"/> is not a primitive and supported type</exception>
        public static T ConvertToType<T>(byte[] value, int startIndex) where T : struct
        {
            ResizeIfNeccesary<T>(ref value, startIndex);
            if (typeof(T) == typeof(byte)) return (T)Convert.ChangeType(value[startIndex], typeof(T));
            else if (typeof(T) == typeof(sbyte)) return (T)Convert.ChangeType(value[startIndex], typeof(T));

            if (MAVLINK_NEED_BYTE_SWAP)
            {
                int sizeOfType = Marshal.SizeOf(default(T));
                Array.Reverse(value, startIndex, sizeOfType);
            }
            if (typeof(T) == typeof(ushort)) return (T)(object)BitConverter.ToUInt16(value, startIndex);
            else if (typeof(T) == typeof(short)) return (T)(object)BitConverter.ToInt16(value, startIndex);
            else if (typeof(T) == typeof(uint)) return (T)(object)BitConverter.ToUInt32(value, startIndex);
            else if (typeof(T) == typeof(int)) return (T)(object)BitConverter.ToInt32(value, startIndex);
            else if (typeof(T) == typeof(ulong)) return (T)(object)BitConverter.ToUInt64(value, startIndex);
            else if (typeof(T) == typeof(long)) return (T)(object)BitConverter.ToInt64(value, startIndex);
            else if (typeof(T) == typeof(float)) return (T)(object)BitConverter.ToSingle(value, startIndex);
            else if (typeof(T) == typeof(double)) return (T)(object)BitConverter.ToDouble(value, startIndex);
            else throw new NotSupportedException($"Unsupported (primitive) type {typeof(T)}");
        }

        /// <summary>
        ///     Converts a byte array to a value array of the expected (primative) type.
        ///     Only the amount of required bytes for the type are evaluated.
        ///     if the provided byte array is not large enough (not enough bytes) for the 
        ///     desired return type, additional bytes will be adde to the end of the byte array.
        /// </summary>
        /// <typeparam name="T">(Primitive) type of the expected return value</typeparam>
        /// <param name="value">Byte array containing a value that need to be converted 
        ///     to a primative type <typeparamref name="T"/></param>
        /// <param name="startIndex">Stating position in the array of the value</param>
        /// <param name="size">Number of values of type <typeparamref name="T"/> that should be 
        ///     extracted from <paramref name="value"/></param>
        /// <returns>Array of values in (primitive) type <typeparamref name="T"/></returns>
        /// <exception cref="NotSupportedException">Thown if <typeparamref name="T"/> is not a primitive and supported type</exception>
        public static T[] ConvertToType<T>(byte[] value, int startIndex, int size) where T : struct
        {
            T[] arr = new T[size];
            int sizeOfType = Marshal.SizeOf(default(T));
            for (int i = 0; i < size; i++)
                arr[i] = ConvertToType<T>(value, startIndex + (i * sizeOfType));
            return arr;
        }
        #endregion Deserialization

        #region Serialization
        /// <summary>
        ///     Converts/serializes a value of a (primative) type <typeparamref name="T"/> to a
        ///     designated byte array.
        ///     if the provided destination byte array is not large enough (not enough bytes) 
        ///     for the desired return type, the result will not be copied and 
        ///     the <paramref name="dst"/> stays untouched.
        /// </summary>
        /// <typeparam name="T">(Primitive) type of the provided value</typeparam>
        /// <param name="value">Value of primative type <typeparamref name="T"/></param>
        /// <param name="dst">Destination array to copy the serialized bytes to</param>
        /// <param name="startIndex">Stating position in the destination array to copy the value to</param>
        /// <exception cref="NotSupportedException">Thown if <typeparamref name="T"/> is not a primitive and supported type</exception>
        public static void ToBytes<T>(T value, byte[] dst, int startIndex) where T : struct
        {
            byte[] bytes;
            if (typeof(T) == typeof(byte)) bytes = new byte[] { (byte)Convert.ChangeType(value, typeof(byte)) };
            else if (typeof(T) == typeof(sbyte)) bytes = new byte[] { (byte)Convert.ChangeType(value, typeof(byte)) };
            else if (typeof(T) == typeof(ushort)) bytes = BitConverter.GetBytes((ushort)Convert.ChangeType(value, typeof(ushort)));
            else if (typeof(T) == typeof(short)) bytes = BitConverter.GetBytes((short)Convert.ChangeType(value, typeof(short)));
            else if (typeof(T) == typeof(uint)) bytes = BitConverter.GetBytes((uint)Convert.ChangeType(value, typeof(uint)));
            else if (typeof(T) == typeof(int)) bytes = BitConverter.GetBytes((int)Convert.ChangeType(value, typeof(int)));
            else if (typeof(T) == typeof(ulong)) bytes = BitConverter.GetBytes((ulong)Convert.ChangeType(value, typeof(ulong)));
            else if (typeof(T) == typeof(long)) bytes = BitConverter.GetBytes((long)Convert.ChangeType(value, typeof(long)));
            else if (typeof(T) == typeof(float)) bytes = BitConverter.GetBytes((float)Convert.ChangeType(value, typeof(float)));
            else if (typeof(T) == typeof(double)) bytes = BitConverter.GetBytes((double)Convert.ChangeType(value, typeof(double)));
            else throw new NotSupportedException($"Unsupported (primitive) type {typeof(T)}");

            if (MAVLINK_NEED_BYTE_SWAP) Array.Reverse(bytes);
            if (dst.Length < startIndex + bytes.Length) return;
            Array.Copy(bytes, 0, dst, startIndex, bytes.Length);
        }

        /// <summary>
        ///     Converts/serializes a value array of a (primative) type <typeparamref name="T"/> 
        ///     to a designated byte array.
        ///     if the provided destination byte array is not large enough (not enough bytes) 
        ///     for the desired return type, the result will not be copied and 
        ///     the <paramref name="dst"/> stays untouched.
        /// </summary>
        /// <typeparam name="T">(Primitive) type of the provided value</typeparam>
        /// <param name="src">Value array of primative type <typeparamref name="T"/></param>
        /// <param name="dst">Destination array to copy the serialized bytes to</param>
        /// <param name="startIndex">Stating position in the destination array to copy the value to</param>
        /// <param name="size">Number of values of type <typeparamref name="T"/> that should be 
        ///     extracted from <paramref name="src"/></param>
        /// <exception cref="NotSupportedException">Thown if <typeparamref name="T"/> is not a primitive and supported type</exception>
        public static void ToBytes<T>(T[] src, byte[] dst, int startIndex, int size) where T : struct
        {
            int sizeOfType = Marshal.SizeOf(default(T));
            for (int i = 0; i < size && i < src.Length; i++)
                ToBytes(src[i], dst, startIndex + (i * sizeOfType));
        }
        #endregion Serialization
    }
}