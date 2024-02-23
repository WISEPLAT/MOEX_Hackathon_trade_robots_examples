// To parse this data:
//
//   import { Convert, NWSZ0N5PTo } from "./file";
//
//   const nWSZ0N5PTo = Convert.toNWSZ0N5PTo(json);
//
// These functions will throw an error if the JSON doesn't
// match the expected interface, even if the JSON is valid.

export interface BackTestResult {
	task_id: string;
	singals_example: SingalsExample;
	test_accuracy_score: BuyHoldSharp;
	test_roc_auc_score: BuyHoldSharp;
	test_precision_score: BuyHoldSharp;
	test_recall_score: BuyHoldSharp;
	test_f1_score: BuyHoldSharp;
	test_log_loss: BuyHoldSharp;
	data_std: BuyHoldSharp;
	max_risk: BuyHoldSharp;
	buy_hold_std: BuyHoldSharp;
	buy_hold_sharp: BuyHoldSharp;
	ideal_strategy_profit_without_shift: BuyHoldSharp;
	ideal_strategy_profit_with_shift: BuyHoldSharp;
	ideal_strategy_std_without_shift: BuyHoldSharp;
	ideal_strategy_std_with_shift: BuyHoldSharp;
	ideal_strategy_sharp_without_shift: BuyHoldSharp;
	ideal_strategy_sharp_with_shift: BuyHoldSharp;
	ideal_strategy_trade_count_without_shift: BuyHoldSharp;
	ideal_strategy_trade_count_with_shift: BuyHoldSharp;
	neural_strategy_profit_without_shift: BuyHoldSharp;
	neural_strategy_profit_with_shift: BuyHoldSharp;
	neural_strategy_std_without_shift: BuyHoldSharp;
	neural_strategy_std_with_shift: BuyHoldSharp;
	neural_strategy_sharp_without_shift: BuyHoldSharp;
	neural_strategy_sharp_with_shift: BuyHoldSharp;
	neural_strategy_trade_count_without_shift: BuyHoldSharp;
	neural_strategy_trade_count_with_shift: BuyHoldSharp;
	dyn_ideal_trading: DynAlTrading;
	dyn_neural_trading: DynAlTrading;
}

export interface BuyHoldSharp {
	description: string;
	value: number;
}

export interface DynAlTrading {
	description: string;
	value: Value;
}

export interface Value {
	Datetime: number[];
	dyn_trades_profit: number[];
	dyn_portfel_profit: number[];
}

export interface SingalsExample {
	markup_signals: MarkupSignals;
	neural_signals: MarkupSignals;
	neural_trends: MarkupSignals;
}

export interface MarkupSignals {
	description: string;
	values: number[];
}

// Converts JSON strings to/from your types
// and asserts the results of JSON.parse at runtime
export class Convert {
	public static toNWSZ0N5PTo(json: string): BackTestResult {
		return cast(JSON.parse(json), r("NWSZ0N5PTo"));
	}

	public static nWSZ0N5PToToJson(value: BackTestResult): string {
		return JSON.stringify(uncast(value, r("NWSZ0N5PTo")), null, 2);
	}
}

function invalidValue(typ: any, val: any, key: any, parent: any = ""): never {
	const prettyTyp = prettyTypeName(typ);
	const parentText = parent ? ` on ${parent}` : "";
	const keyText = key ? ` for key "${key}"` : "";
	throw Error(
		`Invalid value${keyText}${parentText}. Expected ${prettyTyp} but got ${JSON.stringify(
			val,
		)}`,
	);
}

function prettyTypeName(typ: any): string {
	if (Array.isArray(typ)) {
		if (typ.length === 2 && typ[0] === undefined) {
			return `an optional ${prettyTypeName(typ[1])}`;
		} else {
			return `one of [${typ
				.map((a) => {
					return prettyTypeName(a);
				})
				.join(", ")}]`;
		}
	} else if (typeof typ === "object" && typ.literal !== undefined) {
		return typ.literal;
	} else {
		return typeof typ;
	}
}

function jsonToJSProps(typ: any): any {
	if (typ.jsonToJS === undefined) {
		const map: any = {};
		typ.props.forEach(
			(p: any) => (map[p.json] = { key: p.js, typ: p.typ }),
		);
		typ.jsonToJS = map;
	}
	return typ.jsonToJS;
}

function jsToJSONProps(typ: any): any {
	if (typ.jsToJSON === undefined) {
		const map: any = {};
		typ.props.forEach(
			(p: any) => (map[p.js] = { key: p.json, typ: p.typ }),
		);
		typ.jsToJSON = map;
	}
	return typ.jsToJSON;
}

function transform(
	val: any,
	typ: any,
	getProps: any,
	key: any = "",
	parent: any = "",
): any {
	function transformPrimitive(typ: string, val: any): any {
		if (typeof typ === typeof val) return val;
		return invalidValue(typ, val, key, parent);
	}

	function transformUnion(typs: any[], val: any): any {
		// val must validate against one typ in typs
		const l = typs.length;
		for (let i = 0; i < l; i++) {
			const typ = typs[i];
			try {
				return transform(val, typ, getProps);
			} catch (_) {}
		}
		return invalidValue(typs, val, key, parent);
	}

	function transformEnum(cases: string[], val: any): any {
		if (cases.indexOf(val) !== -1) return val;
		return invalidValue(
			cases.map((a) => {
				return l(a);
			}),
			val,
			key,
			parent,
		);
	}

	function transformArray(typ: any, val: any): any {
		// val must be an array with no invalid elements
		if (!Array.isArray(val))
			return invalidValue(l("array"), val, key, parent);
		return val.map((el) => transform(el, typ, getProps));
	}

	function transformDate(val: any): any {
		if (val === null) {
			return null;
		}
		const d = new Date(val);
		if (isNaN(d.valueOf())) {
			return invalidValue(l("Date"), val, key, parent);
		}
		return d;
	}

	function transformObject(
		props: { [k: string]: any },
		additional: any,
		val: any,
	): any {
		if (val === null || typeof val !== "object" || Array.isArray(val)) {
			return invalidValue(l(ref || "object"), val, key, parent);
		}
		const result: any = {};
		Object.getOwnPropertyNames(props).forEach((key) => {
			const prop = props[key];
			const v = Object.prototype.hasOwnProperty.call(val, key)
				? val[key]
				: undefined;
			result[prop.key] = transform(v, prop.typ, getProps, key, ref);
		});
		Object.getOwnPropertyNames(val).forEach((key) => {
			if (!Object.prototype.hasOwnProperty.call(props, key)) {
				result[key] = transform(
					val[key],
					additional,
					getProps,
					key,
					ref,
				);
			}
		});
		return result;
	}

	if (typ === "any") return val;
	if (typ === null) {
		if (val === null) return val;
		return invalidValue(typ, val, key, parent);
	}
	if (typ === false) return invalidValue(typ, val, key, parent);
	let ref: any = undefined;
	while (typeof typ === "object" && typ.ref !== undefined) {
		ref = typ.ref;
		typ = typeMap[typ.ref];
	}
	if (Array.isArray(typ)) return transformEnum(typ, val);
	if (typeof typ === "object") {
		return typ.hasOwnProperty("unionMembers")
			? transformUnion(typ.unionMembers, val)
			: typ.hasOwnProperty("arrayItems")
			  ? transformArray(typ.arrayItems, val)
			  : typ.hasOwnProperty("props")
			    ? transformObject(getProps(typ), typ.additional, val)
			    : invalidValue(typ, val, key, parent);
	}
	// Numbers can be parsed by Date but shouldn't be.
	if (typ === Date && typeof val !== "number") return transformDate(val);
	return transformPrimitive(typ, val);
}

function cast<T>(val: any, typ: any): T {
	return transform(val, typ, jsonToJSProps);
}

function uncast<T>(val: T, typ: any): any {
	return transform(val, typ, jsToJSONProps);
}

function l(typ: any) {
	return { literal: typ };
}

function a(typ: any) {
	return { arrayItems: typ };
}

function u(...typs: any[]) {
	return { unionMembers: typs };
}

function o(props: any[], additional: any) {
	return { props, additional };
}

function m(additional: any) {
	return { props: [], additional };
}

function r(name: string) {
	return { ref: name };
}

const typeMap: any = {
	NWSZ0N5PTo: o(
		[
			{ json: "task_id", js: "task_id", typ: "" },
			{
				json: "singals_example",
				js: "singals_example",
				typ: r("SingalsExample"),
			},
			{
				json: "test_accuracy_score",
				js: "test_accuracy_score",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "test_roc_auc_score",
				js: "test_roc_auc_score",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "test_precision_score",
				js: "test_precision_score",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "test_recall_score",
				js: "test_recall_score",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "test_f1_score",
				js: "test_f1_score",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "test_log_loss",
				js: "test_log_loss",
				typ: r("BuyHoldSharp"),
			},
			{ json: "data_std", js: "data_std", typ: r("BuyHoldSharp") },
			{ json: "max_risk", js: "max_risk", typ: r("BuyHoldSharp") },
			{
				json: "buy_hold_std",
				js: "buy_hold_std",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "buy_hold_sharp",
				js: "buy_hold_sharp",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "ideal_strategy_profit_without_shift",
				js: "ideal_strategy_profit_without_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "ideal_strategy_profit_with_shift",
				js: "ideal_strategy_profit_with_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "ideal_strategy_std_without_shift",
				js: "ideal_strategy_std_without_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "ideal_strategy_std_with_shift",
				js: "ideal_strategy_std_with_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "ideal_strategy_sharp_without_shift",
				js: "ideal_strategy_sharp_without_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "ideal_strategy_sharp_with_shift",
				js: "ideal_strategy_sharp_with_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "ideal_strategy_trade_count_without_shift",
				js: "ideal_strategy_trade_count_without_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "ideal_strategy_trade_count_with_shift",
				js: "ideal_strategy_trade_count_with_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "neural_strategy_profit_without_shift",
				js: "neural_strategy_profit_without_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "neural_strategy_profit_with_shift",
				js: "neural_strategy_profit_with_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "neural_strategy_std_without_shift",
				js: "neural_strategy_std_without_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "neural_strategy_std_with_shift",
				js: "neural_strategy_std_with_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "neural_strategy_sharp_without_shift",
				js: "neural_strategy_sharp_without_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "neural_strategy_sharp_with_shift",
				js: "neural_strategy_sharp_with_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "neural_strategy_trade_count_without_shift",
				js: "neural_strategy_trade_count_without_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "neural_strategy_trade_count_with_shift",
				js: "neural_strategy_trade_count_with_shift",
				typ: r("BuyHoldSharp"),
			},
			{
				json: "dyn_ideal_trading",
				js: "dyn_ideal_trading",
				typ: r("DynAlTrading"),
			},
			{
				json: "dyn_neural_trading",
				js: "dyn_neural_trading",
				typ: r("DynAlTrading"),
			},
		],
		false,
	),
	BuyHoldSharp: o(
		[
			{ json: "description", js: "description", typ: "" },
			{ json: "value", js: "value", typ: 3.14 },
		],
		false,
	),
	DynAlTrading: o(
		[
			{ json: "description", js: "description", typ: "" },
			{ json: "value", js: "value", typ: r("Value") },
		],
		false,
	),
	Value: o(
		[
			{ json: "Datetime", js: "Datetime", typ: a(3.14) },
			{
				json: "dyn_trades_profit",
				js: "dyn_trades_profit",
				typ: a(3.14),
			},
			{
				json: "dyn_portfel_profit",
				js: "dyn_portfel_profit",
				typ: a(3.14),
			},
		],
		false,
	),
	SingalsExample: o(
		[
			{
				json: "markup_signals",
				js: "markup_signals",
				typ: r("MarkupSignals"),
			},
			{
				json: "neural_signals",
				js: "neural_signals",
				typ: r("MarkupSignals"),
			},
			{
				json: "neural_trends",
				js: "neural_trends",
				typ: r("MarkupSignals"),
			},
		],
		false,
	),
	MarkupSignals: o(
		[
			{ json: "description", js: "description", typ: "" },
			{ json: "values", js: "values", typ: a(0) },
		],
		false,
	),
};
