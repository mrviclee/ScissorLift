#include <cstring>
#include <iostream>
#include <string>
#include <vector>

#include <arpa/inet.h>
#include <netdb.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

std::vector<std::string> split(std::string s, std::string sep, int num) {
    std::vector<std::string> rvalue;
    if (sep == "") {
        rvalue.push_back(s);
        return rvalue;
    }

    int start = 0;
    int end = s.find(sep);
    int count = 1;
    while (end != -1) {
        if (num != -1 && count >= num) {
            end = s.size();
            break;
        }
        rvalue.push_back(s.substr(start, end - start));
        start = end + sep.size();
        end = s.find(sep, start);
        count += 1;
    }
    rvalue.push_back(s.substr(start, end - start));

    return rvalue;
}

std::string listen(int socket){
    std::vector<std::string> arr;
    std::string reply(1024, 0);
    while (true) {

        // recv() call tries to get the response from server
        // BUT there's a catch here, the response might take multiple calls
        // to recv() before it is completely received
        // will be demonstrated in another example to keep this minimal
        auto bytes_recv = recv(socket, &reply.front(), reply.size(), 0);
        if (bytes_recv == -1) {
            std::cerr << "Error while receiving bytes\n";
            return "-6";
        }

        arr = split(reply, ":", 2);
        if (arr.size() < 2) {
            std::cerr << "Invalid message from server: " << reply << std::endl;
            continue;
        }

        std::cout << "Type: " << arr.at(0) << ". Msg: " << arr.at(1) << std::endl;
        if (arr.at(0) == "msg"){
             return arr.at(1).substr(0,4);
        }
    }
}

int main(int argc, char *argv[])
{
    // Now we're taking an ipaddress and a port number as arguments to our program
    char ipAddress[] = "raspberrypi";
    char portNum[]  = "6000";

    addrinfo hints, *p;
    memset(&hints, 0, sizeof(hints));
    hints.ai_family   = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    hints.ai_flags    = AI_PASSIVE;

    int gAddRes = getaddrinfo(ipAddress, portNum, &hints, &p);
    if (gAddRes != 0) {
        std::cerr << gai_strerror(gAddRes) << "\n";
        return -2;
    }

    if (p == NULL) {
        std::cerr << "No addresses found\n";
        return -3;
    }

    // socket() call creates a new socket and returns it's descriptor
    int sockFD = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
    if (sockFD == -1) {
        std::cerr << "Error while creating socket\n";
        return -4;
    }

    // Note: there is no bind() call as there was in Hello TCP Server
    // why? well you could call it though it's not necessary
    // because client doesn't necessarily has to have a fixed port number
    // so next call will bind it to a random available port number

    // connect() call tries to establish a TCP connection to the specified server
    int connectR = connect(sockFD, p->ai_addr, p->ai_addrlen);
    if (connectR == -1) {
        close(sockFD);
        std::cerr << "Error while connecting socket\n";
        return -5;
    }

    std::string msg = "Hello World!\n";
    write(sockFD, msg.c_str(), msg.size());

    std::vector<std::string> arr;
    std::string reply(1024, 0);

    
    std::string check_level_cmd = "is_level\n";
    std::string open_cmd = "open\n";
    std::string check_open_cmd = "is_open\n";
    std::string lift_cmd = "lift:100000\n";
    std::string close_cmd = "close\n";

    write(sockFD, check_level_cmd.c_str(), check_level_cmd.size());
    std::string is_level = "";
    std::string opened = "";
    std::string is_open = "";
    std::string lifted = "";

    is_level = listen(sockFD);
    if (is_level != "True"){
        return -1;
    }
    write(sockFD, open_cmd.c_str(), open_cmd.size());
    opened = listen(sockFD);
    if (opened != "True"){
        return -1;
    }
    write(sockFD, check_open_cmd.c_str(), check_open_cmd.size());
    is_open = listen(sockFD);
    if (is_open != "True"){
        return -1;
    }
    write(sockFD, lift_cmd.c_str(), lift_cmd.size());
    lifted = listen(sockFD);
    int lifted_times = 0;
    while(lifted == "time" && lifted_times < 2){
        lifted_times++;
        write(sockFD, lift_cmd.c_str(), lift_cmd.size());
        lifted = listen(sockFD);
    }
    if (lifted != "True"){
        return -1;
    }

    close(sockFD);
    freeaddrinfo(p);

    return 0;
}