import Client

CS3CP_HOST = "127.0.0.1"
CS3CP_PORT = 653

client = Client((CS3CP_HOST, CS3CP_PORT))

resp = client.connect("#user")
print(resp)

resp = client.chat("#musa", "Hi Musa")
print(resp)

if resp == "203 RECEIVED":
    pass
    # wait for delivery
    # modifiedMessage, serverAddress = client_socket.recvfrom(2048)
    # print(modifiedMessage.decode())

resp = client.disconnect()
print(resp)