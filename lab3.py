# LAB 3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Generic, Iterable, Optional, Tuple, TypeVar


A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


# ============================================================
# 10-Question Consolidated Lab (Challenge)
# Sources: lab.py, linked_list_lambda_merge_sort.py, curry_howard_challenge.py
# ============================================================


# Q1
ChurchBool = Callable[[Any], Callable[[Any], Any]]


def church_true(x: Any) -> Callable[[Any], Any]:
    return lambda y: x


def church_false(x: Any) -> Callable[[Any], Any]:
    return lambda y: y


def church_not(b: ChurchBool) -> ChurchBool:
    """Q1: Implement Church boolean negation."""
    # TODO: Return the Church-encoded negation of b.
    # Write your answer below this comment.
    return b(church_false)(church_true)
    raise NotImplementedError("Q1")


def from_church_bool(b: ChurchBool) -> bool:
    return b(True)(False)


# Q2
def compose(f: Callable[[B], C], g: Callable[..., B]) -> Callable[..., C]:
    """Q2: Implement variadic composition: f(g(*args, **kwargs))."""
    # TODO: Return a new function that accepts the arguments for g,
    # then applies f to the result of g.
    # Write your answer below this comment.
    return lambda *args, **kwargs: f(g(*args, **kwargs))
    raise NotImplementedError("Q2")


# Q3
def map_recursive(fn: Callable[[A], B], xs: list[A]) -> list[B]:
    """Q3: Implement recursive map without loops."""
    # TODO: Recursively apply fn to every element of xs.
    # Do not use loops for this question.
    # Write your answer below this comment.
    if not xs:
        return []
    return [fn(xs[0])] + map_recursive(fn, xs[1:])
    raise NotImplementedError("Q3")


# Q4
def fix(f: Callable[[Callable[..., Any]], Callable[..., Any]]) -> Callable[..., Any]:
    """Q4: Implement eager fixed-point combinator (Z-style)."""
    # TODO: Implement a fixed-point combinator that works in eager Python.
    # It should support recursive functions through self-application.
    # Write your answer below this comment.
    return (lambda x: f(lambda *args: x(x)(*args)))(lambda x: f(lambda *args: x(x)(*args)))
    raise NotImplementedError("Q4")


# Q5
class Type:
    pass


@dataclass(frozen=True)
class TInt(Type):
    pass


@dataclass(frozen=True)
class TBool(Type):
    pass


@dataclass(frozen=True)
class TFun(Type):
    arg: Type
    ret: Type


class Expr:
    pass
#tui muốn thay đổi 

@dataclass(frozen=True)
class Var(Expr):
    name: str


@dataclass(frozen=True)
class Lam(Expr):
    param: str
    param_type: Type
    body: Expr


@dataclass(frozen=True)
class App(Expr):
    fn: Expr
    arg: Expr


@dataclass(frozen=True)
class IntLit(Expr):
    value: int


@dataclass(frozen=True)
class BoolLit(Expr):
    value: bool


@dataclass(frozen=True)
class If(Expr):
    cond: Expr
    then_branch: Expr
    else_branch: Expr


@dataclass(frozen=True)
class Add(Expr):
    left: Expr
    right: Expr


@dataclass(frozen=True)
class Sub(Expr):
    left: Expr
    right: Expr


@dataclass(frozen=True)
class Mod(Expr):
    left: Expr
    right: Expr


@dataclass(frozen=True)
class IsZero(Expr):
    value: Expr


TypeEnv = Dict[str, Type]


def type_of(expr: Expr, env: TypeEnv | None = None) -> Type:
    """Q5: Implement type checker for Expr including Add/Sub/Mod/IsZero."""
    # TODO: Return the type of expr under env.
    # Handle literals, variables, lambdas, applications, if-expressions,
    # Add, Sub, Mod, and IsZero.
    # Raise TypeError when an expression is not well-typed.
    # Write your answer below this comment.
    if env is None:
        env = {}
    if isinstance(expr, IntLit):
        return TInt()
    if isinstance(expr, BoolLit):
        return TBool()
    if isinstance(expr, Var):
        if expr.name in env:
            return env[expr.name]
        raise TypeError(f"Undefined variable: {expr.name}")
    if isinstance(expr, Lam):
        new_env = env.copy()
        new_env[expr.param] = expr.param_type
        body_type = type_of(expr.body, new_env)
        return TFun(expr.param_type, body_type)
    if isinstance(expr, App):
        fn_type = type_of(expr.fn, env)
        arg_type = type_of(expr.arg, env)
        if isinstance(fn_type, TFun):
            if fn_type.arg == arg_type:
                return fn_type.ret
            raise TypeError(f"Function expected argument of type {fn_type.arg}, got {arg_type}")
        raise TypeError(f"Attempting to apply non-function of type {fn_type}")
    if isinstance(expr, If):
        cond_type = type_of(expr.cond, env)
        if cond_type != TBool():
            raise TypeError(f"If condition must be boolean, got {cond_type}")
        then_type = type_of(expr.then_branch, env)
        else_type = type_of(expr.else_branch, env)
        if then_type != else_type:
            raise TypeError(f"If branches must have the same type, got {then_type} and {else_type}")
        return then_type
    if isinstance(expr, (Add, Sub, Mod)):
        left_type = type_of(expr.left, env)
        right_type = type_of(expr.right, env)
        if left_type != TInt() or right_type != TInt():
            raise TypeError(f"Arithmetic operations require integer operands, got {left_type} and {right_type}")
        return TInt()
    if isinstance(expr, IsZero):
        value_type = type_of(expr.value, env)
        if value_type != TInt():
            raise TypeError(f"IsZero requires an integer operand, got {value_type}")
        return TBool()
    
    raise NotImplementedError("Q5")


# Q6 + Q7
@dataclass
class Node:
    value: int
    next: Node | None = None


def ll_from_iterable(values: Iterable[int]) -> Node | None:
    head: Node | None = None
    tail: Node | None = None
    for v in values:
        n = Node(v)
        if head is None:
            head = n
            tail = n
        else:
            tail.next = n
            tail = n
    return head


def ll_to_list(head: Node | None) -> list[int]:
    out: list[int] = []
    cur = head
    while cur is not None:
        out.append(cur.value)
        cur = cur.next
    return out


def merge_sorted_lists(a: Node | None, b: Node | None) -> Node | None:
    """Q6: Merge two already sorted linked lists."""
    # TODO: Merge two sorted linked lists into one sorted linked list.
    # You may implement this recursively.
    # Write your answer below this comment.
    if a is None:
        return b
    if b is None:
        return a
    
    if a.value <= b.value:
        a.next = merge_sorted_lists(a.next, b)
        return a
    else:
        b.next = merge_sorted_lists(a, b.next)
        return b
    
    raise NotImplementedError("Q6")


def merge_sort_linked(head: Node | None) -> Node | None:
    """Q7: Implement linked-list merge sort."""
    # TODO: Sort the linked list using merge sort.
    # Split the list, recursively sort each half, then merge them.
    # Write your answer below this comment.
    if head is None or head.next is None:
        return head
    slow = head
    fast = head.next

    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next

    mid = slow.next
    slow.next = None

    left_sorted = merge_sort_linked(head)
    right_sorted = merge_sort_linked(mid)
    return merge_sorted_lists(left_sorted, right_sorted)
    raise NotImplementedError("Q7")


# Q8 + Q9
@dataclass(frozen=True)
class Tree(Generic[A]):
    value: A
    left: Optional[Tree[A]] = None
    right: Optional[Tree[A]] = None


def foldl(fn: Callable[[B, A], B], init: B, xs: Iterable[A]) -> B:
    """Q8: Implement left fold for iterables."""
    # TODO: Traverse xs from left to right, updating the accumulator.
    # Start with init and repeatedly apply fn(acc, x).
    # Write your answer below this comment.
    acc = init
    for x in xs:
        acc = fn(acc, x)
    return acc
    raise NotImplementedError("Q8")


def fold_tree(leaf: B, node_fn: Callable[[A, B, B], B], t: Optional[Tree[A]]) -> B:
    """Q9: Implement structural fold over binary tree."""
    # TODO: Return leaf for an empty tree.
    # For a non-empty tree, recursively fold left and right subtrees,
    # then combine them with node_fn(value, left_result, right_result).
    # Write your answer below this comment.
    if t is None:
        return leaf
    left_folded = fold_tree(leaf, node_fn, t.left)
    right_folded = fold_tree(leaf, node_fn, t.right)
    return node_fn(t.value, left_folded, right_folded)
    raise NotImplementedError("Q9")


# Q10
def q5_curry(h: Callable[[Tuple[A, B]], C]) -> Callable[[A], Callable[[B], C]]:
    """Q10: Implement Curry-Howard currying: ((A,B)->C) -> A -> B -> C."""
    # TODO: Convert a function that takes one pair argument into
    # a curried function that takes a, then b.
    # Write your answer below this comment.
    def curried_a(a: A) -> Callable[[B], C]:
        def curried_b(b: B) -> C:
            return h((a, b))
        return curried_b
    return curried_a
    raise NotImplementedError("Q10")

# import pandas as pd
# import re
# import csv
# import unicodedata
# from rapidfuzz import process, fuzz

# FILE_GOC = 'submission_final.csv'
# FILE_TRAIN = 'train_labels.csv'
# FILE_MOI = 'submission.csv'

# # BẢN ĐỒ KHỬ LỖI MÃ HÓA (Xử lý triệt để các ký tự lạ do lỗi font OCR)
# FONT_FIX_MAP = {
#     'Ä': 'A', 'Ö': 'O', 'Ü': 'U', 'Ã': 'A', 'Å': 'A', 'É': 'E',
#     'ä': 'a', 'ö': 'o', 'ü': 'u', 'ã': 'a', 'å': 'a', 'é': 'e'
# }

# # --- BƯỚC CẢI TIẾN CỐT LÕI: TIỀN XỬ LÝ SỚM (PRE-CLEAN) ---
# def pre_clean_ocr(text):
#     if pd.isna(text): 
#         return ""
    
#     text_str = str(text).lower()
    
#     # 1. Sửa lỗi mã hóa font Tây Âu ngay từ đầu
#     for bad_char, good_char in FONT_FIX_MAP.items():
#         text_str = text_str.replace(bad_char, good_char)
        
#     # 2. Thay thế TẤT CẢ ký tự đặc biệt, dấu câu thành KHOẢNG TRẮNG (Tránh dính chữ như HALONG:CANFOCO)
#     text_str = re.sub(r'[^a-z0-9\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', ' ', text_str)
    
#     # 3. Thu gọn khoảng trắng thừa
#     text_str = re.sub(r'\s+', ' ', text_str).strip()
    
#     return unicodedata.normalize('NFC', text_str)


# # 1. TẠO TỪ ĐIỂN CHUẨN TỪ TẬP TRAIN
# train = pd.read_csv(FILE_TRAIN)
# clean_products = [unicodedata.normalize('NFC', str(p).strip()) for p in train['product_name'].dropna().unique() if str(p).strip() != ""]

# # 2. DANH SÁCH ĐEN & TỪ KHÓA TIN TỨC (Mở rộng thêm các token rác hệ thống)
# BLACKLIST = [
#     'bebop', 'blitz', 'darkzone', 'titbeolaocai', 'dramatic', 'skbet', '60giay', 
#     'tintuc', 'tralink', 'tiktok', 'theanh28', 'hanoinews', 'news', 'cnews', 
#     'artnehp', 'tfedenthro', 'video', 'reels', 'capcut', 'disan', 'linhit', 
#     'thoisu', 'drama', 'so22000', 'fssc22000', '2018fssc22000', 'iso22000',
#     'iso', 'fssc', 'haccp', 'gmp', 'fps', 'update', 'epic', 'gmail', 'com'
# ]

# NEWS_KEYWORDS = [
#     'tamdung', 'hoatdong', 'nhamay', 'chinhthuc', 'thongbao', 
#     'tamdunghoatdong', 'dinhchi', 'batgiu', 'khoatoan'
# ]


# # --- HÀM 1: LÀM SẠCH VÀ PHÂN LOẠI CỘT NHÃN SẢN PHẨM (PRODUCT_NAME) ---
# def smart_fix_final(text_precleaned):
#     if not text_precleaned or text_precleaned == " ":
#         return " "
        
#     ocr_lower = text_precleaned.lower()
#     ocr_nospace = ocr_lower.replace(" ", "")

#     # 🛑 CHIẾN THUẬT HARD-STOP 1: Quét danh sách đen kênh MXH / Drama
#     for trash in BLACKLIST:
#         if trash in ocr_lower or trash in ocr_nospace:
#             return " "

#     # 🛑 CHIẾN THUẬT HARD-STOP 2: Quét ngữ cảnh bài báo tin tức (Nhà máy dừng hoạt động...)
#     for word in NEWS_KEYWORDS:
#         if word in ocr_lower or word in ocr_nospace:
#             return " "

#     # BƯỚC 3: CƠ CHẾ CHẤM ĐIỂM THƯƠNG HIỆU (VOTING WEIGHT)
#     scores = {
#         "Pate Cột Đèn Hải Phòng": 0, "Hạ Long Canfoco": 0, "Highlands Coffee": 0,
#         "Nestlé Nan": 0, "Nestlé Milo": 0, "Vinamilk Dielac Gold": 0,
#         "VISSAN Cá Xốt Cà": 0, "TH True Milk": 0, "Aptamil": 0, "Enfamil": 0, "Vinamilk": 0
#     }

#     if "highland" in ocr_nospace: scores["Highlands Coffee"] += 15
#     if "milo" in ocr_nospace: scores["Nestlé Milo"] += 12
#     if "dielac" in ocr_nospace: scores["Vinamilk Dielac Gold"] += 12
#     if "vissan" in ocr_nospace or "caxotca" in ocr_nospace: scores["VISSAN Cá Xốt Cà"] += 12
#     if "thtrue" in ocr_nospace: scores["TH True Milk"] += 12
#     if "aptamil" in ocr_nospace: scores["Aptamil"] += 12
#     if "enfamil" in ocr_nospace: scores["Enfamil"] += 12
        
#     if "cotden" in ocr_nospace or "patecotden" in ocr_nospace:
#         scores["Pate Cột Đèn Hải Phòng"] += 12
#     elif "pate" in ocr_nospace:
#         scores["Pate Cột Đèn Hải Phòng"] += 4
        
#     if "halong" in ocr_nospace or "canfoco" in ocr_nospace:
#         scores["Hạ Long Canfoco"] += 8

#     words = ocr_lower.split()
#     if 'nan' in words and 'nan' not in ['dan', 'nhan', 'pan', 'ban', 'van']:
#         scores["Nestlé Nan"] += 10
#     if "nestle" in ocr_nospace or "nestlé" in ocr_nospace:
#         if scores["Nestlé Nan"] > 0: scores["Nestlé Nan"] += 5
#         if scores["Nestlé Milo"] > 0: scores["Nestlé Milo"] += 5

#     max_brand = max(scores, key=scores.get)
#     if scores[max_brand] >= 5:
#         if max_brand == "Pate Cột Đèn Hải Phòng" and "highland" in ocr_nospace:
#             return "Highlands Coffee"
#         return max_brand

#     # BƯỚC 4: BỘ LỌC SO KHỚP MỜ FALLBACK
#     clean_words = [w for w in words if w not in BLACKLIST and w not in NEWS_KEYWORDS]
#     ocr_filtered = " ".join([w for w in clean_words if len(w) > 2])
#     if len(ocr_filtered.strip()) < 4:
#         return " "

#     # Đổi sang token_set_ratio để bắt chuỗi con tốt hơn khi dữ liệu nhiễu
#     match = process.extractOne(ocr_filtered, clean_products, scorer=fuzz.token_set_ratio)
#     if match and match[1] >= 75:  
#         if match[0].lower() not in BLACKLIST:
#             return match[0]

#     return " "


# # --- HÀM 2: HẬU XỬ LÝ LỌC SẠCH RÁC TUYỆT ĐỐI CHO CỘT VĂN BẢN (OCR_TEXT) ---
# def final_clean_ocr_column(text_precleaned):
#     if not text_precleaned or text_precleaned == " ":
#         return " "
        
#     words = text_precleaned.split()
    
#     # Loại bỏ từ khóa blacklist, từ khóa tin tức, ký tự đơn lẻ và các token thuần số (ngày tháng, mã số)
#     cleaned_words = [
#         w for w in words 
#         if w not in BLACKLIST 
#         and w not in NEWS_KEYWORDS 
#         and len(w) > 1 
#         and not w.isdigit()
#     ]
    
#     final_text = " ".join(cleaned_words).upper()
#     return final_text.strip() if final_text.strip() != "" else " "


# # --- TIẾN HÀNH THỰC THI XỬ LÝ DỮ LIỆU ĐỒNG BỘ ---
# if __name__ == '__main__':
#     print("🚀 Đang chạy bộ siêu lọc tiền xử lý và dọn rác font chữ song song...")
#     df = pd.read_csv(FILE_GOC)

#     # Bước 1: Tiền xử lý đồng bộ (Khử lỗi font, phá vỡ cấu trúc dính liền của dấu câu)
#     df['ocr_cleaned_temp'] = df['ocr_text'].apply(pre_clean_ocr)

#     # Bước 2: Ép nhãn sản phẩm dựa trên bản chuỗi đã được tiền xử lý chuẩn
#     df['product_name'] = df['ocr_cleaned_temp'].apply(smart_fix_final)

#     # Bước 3: Dọn dẹp nốt rác hệ thống, số cô lập để tạo ra cột ocr_text sạch đẹp nhất
#     df['ocr_text'] = df['ocr_cleaned_temp'].apply(final_clean_ocr_column)

#     # Bước 4: Đồng bộ định dạng khoảng trắng " " theo quy định chấm bài của BTC
#     df['product_name'] = df['product_name'].apply(lambda x: x if (isinstance(x, str) and x.strip() != "") else " ")
#     df['ocr_text'] = df['ocr_text'].apply(lambda x: x if (isinstance(x, str) and x.strip() != "") else " ")

#     # Xóa bỏ cột nháp tạm thời
#     df = df.drop(columns=['ocr_cleaned_temp'])

#     # Xuất file submission chuẩn hóa cuối cùng
#     df.to_csv(FILE_MOI, index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)
#     print(f"🎉 XỬ LÝ HOÀN TẤT! File đầu ra lột xác hoàn toàn sạch đẹp: {FILE_MOI}")
