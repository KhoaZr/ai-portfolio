# BÁO CÁO KỸ THUẬT: Backend Authentication, JWT, Bcrypt và CRUD API trong dự án AI - PORTFOLIO

- **Ngày thực hiện:** [2026-11-09 ; 2026-11-11]
- **Tác giả:** DƯƠNG CÔNG KHOA
- **Phân loại:** Học tập, dự án cá nhân
- **Trạng thái:** Đã hoàn thành 
- **Vai trò:** Người học và làm dự án

---

## 1. BỐI CẢNH & MỤC TIÊU (CONTEXT & OBJECTIVES)

### 1.1. Bối cảnh
Đang tìm hiểu các kiến thức backend cơ bản về Authentication, JWT, Bcrypt và CRUD API nhằm xây dựng hệ thống xác thực người dùng và quản lý dữ liệu thông qua RESTful API.

### 1.2. Mục tiêu
- Hiểu được lý thuyết và cách dùng của authentication, jwt, bcrypt và CRUD API.
- Áp dụng kiến thức vừa học vào dự án và chạy không có lỗi.

### 1.3. Phạm vi thực hiện
- Tìm hiểu cơ chế Authentication và Authorization trong backend.
- Tìm hiểu JWT và Bcrypt trong xác thực người dùng.
- Xây dựng API đăng kí, đăng nhập và xác thực người dùng.
- Áp dụng CRUD API vào dự án.
- Chưa triển khai các cơ chế bảo mật nâng cao.

---

## 2. CÔNG NGHỆ & CÔNG CỤ SỬ DỤNG (TECH STACK & SKILLS)

Liệt kê công nghệ, công cụ và vai trò cụ thể của từng thành phần.

| Công nghệ / Công cụ | Vai trò trong dự án | Mức độ sử dụng |
|---|---|---|
| Python | Ngôn ngữ lập trình backend | - |
| FastAPI | Xây dựng REST API | - |

### 2.1. Công nghệ chính
- **FastAPI:** Xây dựng các API Backend.

### 2.2. Kiến thức và kỹ năng áp dụng
#### Phần 1: Kiến thức về backend authentication
##### 1. Phân biệt Authentication và Authorization 
| Khái niệm | Ý nghĩa | Câu hỏi |
|---|---|---|
| Authentication (AuthN) | Xác thực danh tính| Bạn là ai?|
| Authorization (AuthZ) | Phân quyền truy cập | Bạn được phép làm gì? |

**Ví dụ trong AI Portfolio:**
- Người dùng đăng nhập bằng username và password -> Authentication
- Người dùng chỉ được chỉnh sửa thông tin cá nhân của mình -> Authorization
- Admin được phép quản lý tất cả dự án -> Authorization

**Ghi nhớ:** Authentication xác định danh tính còn Authorization xác định quyền hạn.


##### 2. Password Hashing - Bcrypt
###### 2.1. Tại sao không lưu mật khẩu trực tiếp?
Giả sử người dùng đăng kí:

| Username | Password |  
|---|---|
| khoa | khoa123456 |
| admin | admin123 |

Nếu database lưu trực tiếp mật khẩu, khi database bị lộ, kẻ tấn công có thể biết ngay thông tin đăng nhập của người dùng -> Giải pháp là sử dụng password hashing.

###### 2.2. Hashing là gì?
Hashing là quá trình chuyển đổi dữ liệu đầu vào thành một chuỗi có độ dài và định dạng nhất định bằng thuật toán băm.  
Điểm quan trọng: 
- Hashing là một chiều, không thể giải mã ngược như mã hóa thông thường.
- Cùng một mật khẩu có thể tạo ra nhiều hash khác nhau do salt.
- Khi đăng nhập, hệ thống sẽ kiểm tra mật khẩu nhập vào với hash đã lưu.


###### 2.3. Salt là gì?
Salt là một chuỗi dữ liệu ngẫu nhiên được thêm vào quá trình hashing.  
**Ví dụ:**
| Người dùng| Password | Salt | Hash |
| --- | --- | --- | --- |
| A | 123456 | A | A | 
| B | 123456 | B | B | 

Dù 2 người có mật khẩu giống nhau thì hash vẫn khác nhau.  
Bcrypt tự xử lý Salt và lưu thông tin Salt trong chuỗi hash. Mình không cần tự thiết kế cơ chế này.



###### 2.4. Cách Bcrypt xác minh mật khẩu
Khi đăng nhập:   
1. Người dùng gửi username và password..
2. Backend tìm người dùng trong database.
3. Lấy password hash đã lưu.
4. Bcrypt sử dụng cơ chế verify để kiểm tra mật khẩu nhập vào.
5. Nếu đúng, tiếp tục JWT.
6. Nếu sai, trả về lỗi xác thực.

##### 3. JWT (Json web token)
###### 3.1. JWT là gì?
JWT là một tiêu chuẩn token dùng để truyền tải thông tin dưới dạng JSON được ký số.  
Trong Backend Authentication, JWT thường được dùng để xác thực các request sau khi người dùng đăng nhập.  

**Ví dụ:**  
Người dùng đăng nhập thành công -> backend tạo JWT -> Client lưu token -> Client gửi token trong những request tiếp theo.

###### 3.2. Cấu trúc JWT
JWT gồm 3 thành phần:  
1. Header: Chứa thuật toán ký và loại token. Ví dụ: HS256
2. Payload: Chứa các thông tin (Claims) về người dùng và token.  
Một số Claims phổ biến:  

    | Claim | Ý Nghĩa |
    |---|---|
    | sub | subject - id người dùng |
    | exp | thời điểm token hết hạn |
    | iat | Thời điểm token được tạo |
    | iss | Đơn vị phát hành token |
    | aud | Đối tượng được nhận token |
    | role | Vai trò của người dùng  |

3. Signature: Chữ kí được tạo từ header, payload và secret key (đối với thuật toán HMAC).  
Mục đích:  
- Kiểm tra xem token có bị chỉnh sửa không.
- Xác minh token được ký bởi bên kia có khóa bí mật tương ứng.  
**Lưu ý quan trọng:** JWT thông thường chỉ được mã hóa Base64URL ở phần Header và Payload, không phải mã hóa bí mật. Người nhận có thể đọc nội dung payload. Vì vậy, không đưa password, API key hoặc thông tin nhạy cảm vào JWT.

##### 4. Access token và refresh token.  
Đây là hai loại token rất quan trọng trong hệ thống thực tế.  
| Tiêu chí | Access Token | Refresh token |
|---|---|---| 
| Mục đích | Truy cập API | Cấp Access token |
| Thời hạn | Ngắn | Dài hơn |
| Tần suất sử dụng | Thường xuyên | Khi access token hết hạn |
| Bảo mật| Cao | Cần được bảo vệ rất chặt |
Ví dụ tham khảo:  
Access token: 15 phút.  
Refresh Token: 7 ngày.


Luồng hoạt động:
```
        1. Client đăng nhập
        Usernname + password
                      

        2. Backend xác thực
        Kiểm tra password bằng Bcrypt


        3. Cấp 2 token
        Access token | Refresh token
        15 phút      | 7 ngày


        4. Client gửi access token
        Authorization: Bearer TOKEN


        5. Backend xác minh JWT
        Chữ kí, thời hạn, claims và quyền truy cập


        AUTHENTICATED
        CHO PHÉP TRUY CẬP API
```

Khi access token hết hạn:  
1. Client gửi Refresh token đến API Refresh.
2. Backend xác minh refresh token.
3. Nếu hợp lệ, cấp access token mới.
4. Nếu refresh token cũng hết hạn hoặc hị thu hồi, yêu cầu đăng nhập lại.

Trong hệ thống production nên có cơ chế lưu trữ, thu hồi và xoay vòng refresh token (refresh token rotation).

##### 5. Middleware và Dependency authentication.
Một thành phần quan trọng trong backend là Middleware hoặc dependency.  
Nó giúp kiểm tra người dùng trước khi cho phép truy cập các API được bảo vệ 

**Ví dụ:** Người dùng gửi request: `Get /api/v1/users/me`  
Backend sẽ:  
1. Nhận JWT từ header.
2. Kiểm tra token có tồn tại không.
3. Xác minh chữ ký. 
4. Kiểm tra thời hạn.
5. Lấy User ID từ claims `sub`
6. Xác định người dùng tương ứng.
7. Cho phép API tiếp tục xử lý.


Trong FastAPI thường sử dụng Dependency injection.  
Trong Express thường sử dụng Middleware.

##### 6. Các API Authentication cốt lõi

| Method | Endpoint | Chức năng |
|---|---|---|
| POST | `/auth/register` | Đăng ký |
| POST | `/auth/login` | Đăng nhập |
| POST | `/auth/refresh` | Làm mới access token |
| POST | `/auth/logout` | Đăng xuất / thu hồi Refresh Token |
| GET | `/auth/me` | Lấy thông tin người dùng hiện tại |

**Lưu ý:** `/auth/me` là endpoint lấy thông tin người dùng đã xác thực, chứ không phải endpoint đăng nhập.



#### Phần 2: RESTful API và CRUD cốt lõi
##### 7. RESTful API là gì?
REST (Representational state transfer) là một phong cách kiến trúc được dùng để thiết kế API.

RESTful API giúp frontend và backend giao tiếp với nhau thông qua HTTP.


Ví dụ trong AI - portfolio:  
- FE hiện thị danh sách dự án.
- FE gửi HTTP request đến BE FastAPI
- BE truy vấn PostgreSQL.
- BE trả về HTTP response dạng Json.
- Frontend nhận dữ liệu và hiện thị lên giao diện.


###### 7.1. Các thành phần của HTTP Request
Một HTTP request thường có 5 thành phần:  
| Thành Phần | Chức năng |
|------------|-----------|
| method | Hành động muốn thực hiện |
| URL | Địa chỉ API |
| Headers | Thông tin bổ sung |
| Query Parameters | Tham số truy vấn |
| Request Body | Dữ liệu gửi lên backend |

Ví dụ trong một request đăng nhập:  
- Methods: POST
- URL: /api/v1/auth/login
- Headers: Content-type: application/json
- Body: username và password.


###### 7.2 Các thành phần của HTTP response
| Thành phần | Chức năng |
|---|---|
| Status code | Kết quả xử lý |
| Headers | Metadata của response |
| Response Body | Dữ liệu trả về |

Ví dụ:  
- status code: 200 OK
- Response Body: Thông tin người dùng và token.

##### 8. CRUD là gì?
C: Create - POST: Tạo dữ liệu mới.  
R: Read - GET: Đọc dữ liệu.  
U: Update - PUT/PATCH: Cập nhật dữ liệu.  
D: Delete - DELETE: Xóa dữ liệu.


#### Phần 3: Những kiến thức Backend bắt buộc đi kèm với CRUD.
##### 9. HTTP status code
BE cần trả về status code chính xác đề FE biết kết quả xử lý request.

Các mã quan trọng cần nhớ:   
| Status | Tên | Ý nghĩa |
|---|---|---|
| 200 | OK | request thành công |
| 201 | Create | Tạo dữ liệu thành công |
| 204 | No content | Thành công, không có response body |
| 400 | Bad request | Request không hợp lệ |
| 401 | Unahthorized | Chưa xác thực hoặc thông tin xác thực không hợp lệ |
| 403 | Forbidden | Đã xác thực thành công nhưng không đủ quyền |
| 404 | Not Found | Không tìm thấy tài nguyên |
| 409 | Conflict | Xung đột dữ liệu |
| 422 | Unprocessable | Dữ liệu không qua validation |
| 429 | Too many request | Gửi request quá nhiều |
| 500 | Internal Server | Lỗi nội bộ Backend |

Phân biệt 401 và 403:  
- 401: Bạn chưa chứng minh được mình là ai.
- 403: Backend biết bạn là ai nhưng bạn không được phép hành động này.


##### 10. Các vấn đề bảo mật khác.
| Kiến thức | Mục đích |
|---|---|
| HTTPS | Mã hóa dữ liệu khi truyền tải |
| CORS | Kiểm soát nguồn gốc được phép truy cập API | 
| Rate Limiting | Giới hạn số lượng request |
| SQL injection | Ngăn chặn truy vẫn SQL độc hại |
| XSS | Ngăn chặn thực thi Script độc hại |
| CSRF | Ngăn chặn request giả mạo trong một số mô hình xác thực |
| Secret Management | Bảo vệ Secret và database credentials |
| Password Police | Thiết lập yêu cầu mật khẩu |
| Token revocation | Thu hồi Token |
| Audit Log | Ghi nhận hoạt động quan trọng |



---

## 3. QUÁ TRÌNH TRIỂN KHAI & CHỨNG CỨ THỰC HÀNH (IMPLEMENTATION & EVIDENCE)

Mô tả những công việc thực tế đã thực hiện. Ưu tiên bằng chứng có thể kiểm chứng.

### 3.1. Các bước triển khai

**Bước 1: Cài đặt thư viện mật mã và JWT**
- Mô tả: Cài đặt `passlib` (để băm mật khẩu bằng thuật toán Bcrypt) và PyJWT (để sinh mã JSON WEB Token):
```text
uv add "passlib[bcrypt]" pyjwt
```
- Kết quả: passlib và pyjwt đã được cài và dependencies được cập nhật trong file .toml
- Công nghệ sử dụng: uv

**Bước 2: Viết module xử lý mật khẩu và token**
- Mô tả: Viết file security.py để chứa các hàm mã hóa mật khẩu và tạo JWT token.
- Kết quả: Đã có 3 hàm trong file gồm: 1 hàm kiểm tra mật khẩu có khớp với chuỗi băm trong DB hay không?, 1 hàm tạo access token thông tin và thời hạn, 1 hàm băm mật khẩu thô thành chuỗi hash Bcrypt. 
- Công nghệ sử dụng: Thư viện passlib, jwt của ngôn ngữ lập trình python.

**Bước 3: Định nghĩa Schema Pydantic cho Auth**
- Mô tả: Viết file app/schemas/auth.py để kiểm soát dữ liệu đầu vào và đầu ra khi đăng nhập.
- Kết quả: Login request: Dữ liệu đăng nhập; Token response: Dữ liệu JWT trả về sau khi đăng nhập
- Công nghệ sử dụng: pydantic.

**Bước 4: Tạo Dependency bảo vệ các Route Admin**
- Mô tả: Viết file app/core/deps.py Đây là middleware kiểc tra xem request gửi lên có đính kèm Header Authorization: Bearer token hợp lệ hay không
- Kết quả: Xây dựng Dependency xác thực JWT từ header authorization, kiểm tra token hợp lệ và xác định quyền truy cập admin
- Công nghệ sử dụng: auth2passwordBearer, pyJWT, SQLAlchemy.

**Bước 5: Viết API đăng nhập**
- Mô tả: Viết file app/routers/auth.py 
- Kết quả: Đã xây được endpoint auth/login để đăng nhập cùng kiểm tra xem mật khẩu và tài khoản.
- Công nghệ sử dụng: APIRouter, SQLAlchemy, pydantic và Bcrypt

**Bước 6: Viết script tạo tài khoản admin ban đầu**
- Mô tả: Viết file scripts/create_admin.py. Sau đó chạy file để tạo admin:
```text
uv run python scripts/create_admin.py
```
- Kết quả: Xây dựng được script khởi tạo admin ban đầu, mã hóa mật khẩu trước khi lưu vào cơ sở dữ liệu.
- Công nghệ sử dụng: python, SQLAlchemy, Bcrypt, PostgreSQL

**Bước 7: Đăng kí Router**
- Mô tả: Cập nhật file app/main.py và kiểm tra Router được bảo vệ 
- Kết quả: Đã đăng kí Router vào ứng dụng FastAPI
- Công nghệ sử dụng: FastAPI, APIRouter


### 3.2. Kiến trúc và thiết kế kỹ thuật
[Mô tả kiến trúc hệ thống, luồng dữ liệu, cấu trúc database hoặc thuật toán.]

### 3.3. Chứng cứ thực hành (Evidence)

| Loại bằng chứng | Mô tả | Đường dẫn / Link |
|---|---|---|
| Screenshot | Ảnh kết quả khi đã tạo tài khoản admin | ![alt text](image.png) |
| Database | Bảng hoặc dữ liệu đã tạo | ![alt text](image-1.png) |

---

## 4. THÁCH THỨC & BÀI HỌC KINH NGHIỆM (CHALLENGES & KEY LEARNINGS)

### 4.1. Thách thức gặp phải
- **Vấn đề:** Khi chạy script tạo tài khoản admin ở bước 6 tôi gặp phải: 
1. Mapper 'Mapper[SkillEvidence(skill_evidences)]' has no property 'skill'. Mapper 'Mapper[Project(projects)]' has no property 'evidences'. 

2. (trapped) error reading bcrypt version.. 
AttributeError: module 'bcrypt' has no attribute '__about__'

- **Nguyên nhân:** 
1. Do tôi chưa thiêt lập quan hệ relationship thuộc tính skill, project trong bảng SkillEvidence 

2. Phiên bản bcrypt mới đã thay đổi cách cung cấp thông tin phiên bản, trong khi passlib đang sử dụng cách truy cập cũ.

- **Ảnh hưởng:** Làm cho script không thể tạo được admin và báo lỗi.

### 4.2. Giải pháp xử lý
- **Phương pháp:** Đọc logs lỗi, sau đó tìm ra lỗi bằng cách hỏi AI.
- **Các bước thực hiện:** 
 1. Kiểm tra lại bảng skill_evidences. Sau đó hỏi AI cách sửa. 
 2. Cố định phiên bản của bcrypt tương thích
 ```text
uv add "bcrypt==4.0.1"
 ```
- **Kết quả:** Đã tạo được admin và không còn lỗi.

---

## 5. KẾT QUẢ & ĐÁNH GIÁ (RESULTS & EVALUATION)

### 5.1. Kết quả đạt được
- Nắm được kiến thức cơ bản về Authentication, Authorization, JWT và Bcrypt.
- Tạo được tài khoản admin ban đầu và lưu mật khẩu dưới dạng Bcrypt Hast trong PostgreSQL.
- Khắc phục được các lỗi phát sinh trong quá trình triển khai và chạy thành công hệ thống. 

### 5.2. Đánh giá mức độ thành thạo

| Công nghệ / Kỹ năng | Điểm tự đánh giá (1.0 - 5.0) | Cơ sở đánh giá |
|---|---:|---|
| pyhton | 4.0 | Viết được script và xử lý logic backend |
| FastAPI | 3.0 | Xây dựng được API |
| JWT / pyJWT | 4.0 | Tạo và xác thực access token |
| Bcrypt | 3.0 | Hash và xác minh mật khẩu |
| SQLAlchemy | 4.0 | Truy vấn và tương tác với database |

### 5.3. Hạn chế hiện tại
- Chưa triển khai refresh token và cơ chế thu hồi token.
- Chưa có cơ chế Rate Limiting để hạn chế đăng nhập nhiều lần.
- Chưa triển khai đầy đủ các API CRUD và bảo mật nâng cao.

---
