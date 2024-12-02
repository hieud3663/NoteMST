const toJson = (values = []) => {
    // if (!values || values.length <= 1) return [];
    const [keys, ...data] = values;

    // Nếu data rỗng, trả về một mảng có đối tượng với các trường là chuỗi rỗng
    if (data.length === 0) {
        const emptyObject = {};
        keys.forEach(key => {
            emptyObject[key] = ""; // Gán mỗi trường là chuỗi rỗng
        });
        return JSON.stringify([emptyObject]); // Trả về mảng chứa đối tượng có các trường là chuỗi rỗng
    }


    const result = data.map(
        (row) => {
            const object = {};
            keys.forEach((key, index) => object[key] = row[index]);
            return object;
        }
    );
    return JSON.stringify(result);
};

//lấy dữ liệu
const doGet = () => {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    const json = toJson(sheet.getDataRange().getValues());
    return ContentService.createTextOutput(json).setMimeType(ContentService.MimeType.JSON);
};

//gửi dữ liệu
const doPost = (e) => {
    try {
        const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
        const data = JSON.parse(e.postData.contents); // Parse dữ liệu JSON từ yêu cầu POST

        // Lấy ID hiện tại lớn nhất
        const lastRow = sheet.getLastRow();
        const lastId = lastRow > 1 ? sheet.getRange(lastRow, 1).getValue() : 0; // Nếu không có dòng nào, ID bắt đầu từ 0
        const newId = lastId + 1;

        // Tạo một hàng mới từ dữ liệu gửi lên
        const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
        const newRow = headers.map(header => (header === "id" ? newId : String(data[header]) || ""));

        // Ghi dữ liệu vào sheet
        // sheet.appendRow(newRow);

        // Chèn dữ liệu vào hàng mới
        const nextRow = lastRow + 1;
        sheet.insertRowAfter(lastRow); // Chèn hàng mới

        // Đặt định dạng toàn bộ hàng là văn bản
        const range = sheet.getRange(nextRow, 1, 1, newRow.length);
        range.setNumberFormat('@'); // Định dạng tất cả ô trong hàng thành văn bản
        range.setValues([newRow]); // Ghi toàn bộ hàng vào sheet

        

        // Trả về phản hồi JSON
        return ContentService
            .createTextOutput(JSON.stringify({ status: "success", message: "Data added successfully", id: newId, code: 1 }))
            .setMimeType(ContentService.MimeType.JSON);
    } catch (error) {
        return ContentService
            .createTextOutput(JSON.stringify({ status: "error", message: error.message, code: 0 }))
            .setMimeType(ContentService.MimeType.JSON);
    }
};

//edit data
const doPost2 = (e) => {
    try {
        const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
        const data = JSON.parse(e.postData.contents); // Parse dữ liệu JSON từ yêu cầu POST

        const mst = data["mst"]; // Lấy MST từ dữ liệu gửi lên
        if (!mst) {
            throw new Error("MST is missing");
        }

        const headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0]; // Lấy tiêu đề cột
        const mstIndex = headers.indexOf("mst"); // Tìm vị trí của cột MST

        if (mstIndex === -1) {
            throw new Error("MST column not found");
        }

        const lastRow = sheet.getLastRow();
        let foundRow = null;

        // Duyệt qua các hàng để tìm MST khớp
        for (let i = 2; i <= lastRow; i++) { // Bắt đầu từ hàng 2 (hàng 1 là tiêu đề)
            const rowMST = sheet.getRange(i, mstIndex + 1).getValue(); // Lấy giá trị MST của hàng hiện tại
            if (String(rowMST) === String(mst)) {
                foundRow = i;
                break;
            }
        }

        if (foundRow) {
            // Cập nhật dữ liệu ở hàng tìm được
            const updatedRow = headers.map(header => (header === "id" ? sheet.getRange(foundRow, 1).getValue() : String(data[header]) || ""));
            const range = sheet.getRange(foundRow, 1, 1, updatedRow.length);
            range.setValues([updatedRow]); // Ghi đè dữ liệu vào hàng hiện có

            return ContentService
                .createTextOutput(JSON.stringify({ status: "success", message: "Data updated successfully", mst, code: 1 }))
                .setMimeType(ContentService.MimeType.JSON);
        } else {
            return ContentService
                .createTextOutput(JSON.stringify({ status: "error", message: "MST not found", code: 0 }))
                .setMimeType(ContentService.MimeType.JSON);
        }
    } catch (error) {
        return ContentService
            .createTextOutput(JSON.stringify({ status: "error", message: error.message, code: 0 }))
            .setMimeType(ContentService.MimeType.JSON);
    }
};

